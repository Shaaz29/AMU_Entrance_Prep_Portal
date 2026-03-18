import pandas as pd
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
    df = pd.read_excel(file)
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
            concept=_clean_cell(row.get('concept')),
        )
        created_count += 1

    return created_count