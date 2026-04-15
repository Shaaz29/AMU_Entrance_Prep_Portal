import pandas as pd
import zipfile
import io
import os
import concurrent.futures
import time
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import transaction
from .models import Question, MockTest


def _clean_cell(value):
    if pd.isna(value):
        return ''
    return str(value).strip()


def _to_int(value):
    cleaned = _clean_cell(value)
    if not cleaned:
        return None
    try:
        return int(float(cleaned))
    except (ValueError, TypeError):
        return None


def upload_to_cloud(file_path, image_data):
    """Helper purely for threading the I/O Cloudinary upload."""
    retries = 3
    for attempt in range(retries):
        try:
            saved_path = default_storage.save(file_path, ContentFile(image_data))
            return default_storage.url(saved_path)
        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(1)

def import_questions(file, mocktest_id=None):
    is_zip = file.name.lower().endswith('.zip')
    excel_file = None
    zfile = None

    if is_zip:
        zfile = zipfile.ZipFile(file)
        for name in zfile.namelist():
            if name.lower().endswith('.xlsx') and not name.startswith('__MACOSX'):
                excel_file = io.BytesIO(zfile.read(name))
                break
        if not excel_file:
            raise ValueError("No .xlsx file found inside the ZIP archive.")
    else:
        excel_file = file

    df = pd.read_excel(excel_file)
    df.columns = [str(col).strip().lower() for col in df.columns]

    fallback_mocktest = None
    if mocktest_id:
        fallback_mocktest = MockTest.objects.get(id=mocktest_id)

    questions_to_create = []
    
    # 1. First Pass: Read everything into memory, read from zip (sync), queue uploads (async)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        
        for _, row in df.iterrows():
            row_mocktest_id = _to_int(row.get('mocktest'))
            target_mocktest = None

            if row_mocktest_id is not None:
                target_mocktest = MockTest.objects.get(id=row_mocktest_id)
            elif fallback_mocktest is not None:
                target_mocktest = fallback_mocktest
            else:
                raise ValueError("Each row must include a valid 'mocktest' id when no test is selected in the upload form.")

            correct_answer = _clean_cell(row.get('correct_answer')).upper()
            if correct_answer not in {'A', 'B', 'C', 'D'}:
                raise ValueError("'correct_answer' must be one of A, B, C, or D.")

            q_data = {
                'mocktest': target_mocktest,
                'type': 'MCQ',
                'text': _clean_cell(row.get('question')),
                'option_a': _clean_cell(row.get('option_a')),
                'option_b': _clean_cell(row.get('option_b')),
                'option_c': _clean_cell(row.get('option_c')),
                'option_d': _clean_cell(row.get('option_d')),
                'correct_answer': correct_answer,
                'explanation': _clean_cell(row.get('explanation')),
                'image_pieces': [],
                'explanation_image_pieces': []
            }
            
            # Inner helper to process images for a specific cell string
            def schedule_images(val_str, field_key):
                if not val_str:
                    return
                for piece in val_str.split(','):
                    piece = piece.strip()
                    if not piece: continue
                    
                    found_in_zip = False
                    if zfile:
                        search_name = os.path.basename(piece)
                        matching_names = [n for n in zfile.namelist() if n.endswith(search_name) and not n.startswith('__MACOSX')]
                        if matching_names:
                            actual_name = matching_names[0]
                            # Read bytes SYNCHRONOUSLY from the zip file (thread safe)
                            image_data = zfile.read(actual_name)
                            clean_filename = os.path.basename(search_name)
                            file_path = f"questions/{clean_filename}"
                            # Fire thread for the extremely slow Cloudinary API upload
                            future = executor.submit(upload_to_cloud, file_path, image_data)
                            q_data[field_key].append({'type': 'future', 'val': future})
                            found_in_zip = True
                            
                    if not found_in_zip:
                        # E.g. raw urls or filenames without zip
                        q_data[field_key].append({'type': 'string', 'val': piece})

            # Schedule main images and explanation images
            schedule_images(_clean_cell(row.get('image')), 'image_pieces')
            schedule_images(_clean_cell(row.get('explanation_image')), 'explanation_image_pieces')

            questions_to_create.append(q_data)

        # The 'with ThreadPoolExecutor' block waits for all futures to naturally finish before exiting!
        # So by the time we reach here, ALL 150+ Cloudinary uploads have finished efficiently.

    # 2. Second Pass: Insert precisely into the DB!
    created_count = 0
    with transaction.atomic():
        for q_data in questions_to_create:
            
            def resolve_pieces(piece_list):
                resolved = []
                for p in piece_list:
                    if p['type'] == 'future':
                        # Result is instantly available because block is done
                        resolved.append(p['val'].result())
                    else:
                        resolved.append(p['val'])
                return ",".join(resolved) if resolved else ""

            Question.objects.create(
                mocktest=q_data['mocktest'],
                type=q_data['type'],
                text=q_data['text'],
                option_a=q_data['option_a'],
                option_b=q_data['option_b'],
                option_c=q_data['option_c'],
                option_d=q_data['option_d'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation'],
                image=resolve_pieces(q_data['image_pieces']),
                explanation_image=resolve_pieces(q_data['explanation_image_pieces']),
            )
            created_count += 1

    return created_count