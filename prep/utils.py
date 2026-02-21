import pandas as pd
from .models import Question, MockTest

def import_questions(file, mocktest_id):
    df = pd.read_excel(file)

    mocktest = MockTest.objects.get(id=mocktest_id)

    for _, row in df.iterrows():
        Question.objects.create(
            mocktest=mocktest,
            type=row['type'],
            text=row['question'],
            option_a=row.get('option_a', ''),
            option_b=row.get('option_b', ''),
            option_c=row.get('option_c', ''),
            option_d=row.get('option_d', ''),
            correct_answer=row['correct_answer'],
            explanation=row.get('explanation', '')
        )