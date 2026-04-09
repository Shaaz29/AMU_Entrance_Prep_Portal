import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amu_portal.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage

print(f"STORAGES: {settings.STORAGES}")
print(f"Default storage class: {default_storage.__class__}")
print(f"media_url: {settings.MEDIA_URL}")
print(f"CLOUDINARY_URL: {os.environ.get('CLOUDINARY_URL')}")
