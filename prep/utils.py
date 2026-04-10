import pandas as pd
import zipfile
import io
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
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

    created_count = 0

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

        image_val = _clean_cell(row.get('image'))
        
        saved_image_urls = []
        if image_val:
            for piece in image_val.split(','):
                piece = piece.strip()
                if not piece:
                    continue
                
                saved_url = piece
                if zfile:
                    search_name = os.path.basename(piece)
                    matching_names = [n for n in zfile.namelist() if n.endswith(search_name) and not n.startswith('__MACOSX')]
                    if matching_names:
                        actual_name = matching_names[0]
                        image_data = zfile.read(actual_name)
                        clean_filename = os.path.basename(search_name)
                        file_path = f"questions/{clean_filename}"
                        saved_path = default_storage.save(file_path, ContentFile(image_data))
                        saved_url = default_storage.url(saved_path)
                        
                saved_image_urls.append(saved_url)
                
        saved_image_path = ",".join(saved_image_urls) if saved_image_urls else ""

        expl_image_val = _clean_cell(row.get('explanation_image'))
        
        saved_expl_urls = []
        if expl_image_val:
            for piece in expl_image_val.split(','):
                piece = piece.strip()
                if not piece: 
                    continue
                
                saved_url = piece # default to original value 
                if zfile:
                    search_expl_name = os.path.basename(piece)
                    matching_names = [n for n in zfile.namelist() if n.endswith(search_expl_name) and not n.startswith('__MACOSX')]
                    if matching_names:
                        actual_name = matching_names[0]
                        image_data = zfile.read(actual_name)
                        clean_filename = os.path.basename(search_expl_name)
                        file_path = f"questions/{clean_filename}"
                        saved_path = default_storage.save(file_path, ContentFile(image_data))
                        saved_url = default_storage.url(saved_path)
                        
                saved_expl_urls.append(saved_url)
                
        saved_expl_image_path = ",".join(saved_expl_urls) if saved_expl_urls else ""

        Question.objects.create(
            mocktest=target_mocktest,
            type='MCQ',
            text=_clean_cell(row.get('question')),
            option_a=_clean_cell(row.get('option_a')),
            option_b=_clean_cell(row.get('option_b')),
            option_c=_clean_cell(row.get('option_c')),
            option_d=_clean_cell(row.get('option_d')),
            correct_answer=correct_answer,
            explanation=_clean_cell(row.get('explanation')),
            image=saved_image_path,
            explanation_image=saved_expl_image_path,
        )
        created_count += 1

    return created_count