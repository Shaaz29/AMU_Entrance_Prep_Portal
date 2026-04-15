import os
import django
import pandas as pd
import zipfile
import io
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amu_portal.settings')
django.setup()

from prep.utils import import_questions
from prep.models import MockTest, Course

# Create course and mocktest strictly for local diagnosis
c, _ = Course.objects.get_or_create(name='Test Course Local')
m, _ = MockTest.objects.get_or_create(course=c, year='2024', duration=60)

# 2. Create a dummy excel file in memory
df = pd.DataFrame({
    'mocktest': [m.id],
    'question': ['What is 2+2?'],
    'option_a': ['3'],
    'option_b': ['4'],
    'option_c': ['5'],
    'option_d': ['6'],
    'correct_answer': ['B'],
    'explanation': ['Basic math.'],
    'image': ['',],
    'explanation_image': ['',]
})

excel_io = io.BytesIO()
df.to_excel(excel_io, index=False)
excel_io.seek(0)

# 3. Create a dummy ZIP
zip_io = io.BytesIO()
with zipfile.ZipFile(zip_io, 'w') as zf:
    zf.writestr('test.xlsx', excel_io.read())
zip_io.seek(0)
zip_io.name = "dummy.zip"

print(f"Testing import_questions with dummy zip against MockTest ID {m.id}...")
try:
    count = import_questions(zip_io, mocktest_id=m.id)
    print(f"Success! Inserted {count} questions.")
except Exception as e:
    import traceback
    traceback.print_exc()
