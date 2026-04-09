import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amu_portal.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

print(f"Executing with default_storage: {default_storage.__class__}")
try:
    path = default_storage.save("questions/test_file.txt", ContentFile(b"hello cloudinary"))
    print(f"Path saved: {path}")
    url = default_storage.url(path)
    print(f"URL: {url}")
except Exception as e:
    print(f"Exception: {e}")
