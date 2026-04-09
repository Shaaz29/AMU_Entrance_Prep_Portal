import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amu_portal.settings')
django.setup()

from prep.models import Question

q = Question.objects.order_by('-id').first()
if q:
    print(f"ID: {q.id}")
    print(f"Text: {q.text}")
    print(f"Image: {q.image}")
    print(f"Image URL: {q.image_url}")
    print(f"Explanation Image: {q.explanation_image}")
    print(f"Explanation URL: {q.explanation_image_url}")
else:
    print("No questions found.")
