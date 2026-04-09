import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amu_portal.settings')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

png_header = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\xfa\x0f\x00\x01\x05\x01\x02\x15b\xb9\x05\x00\x00\x00\x00IEND\xaeB`\x82"

try:
    path = default_storage.save("questions/test_file.png", ContentFile(png_header))
    url = default_storage.url(path)
    print(f"URL from default_storage.url(): {url}")
except Exception as e:
    print(f"Exception: {e}")
