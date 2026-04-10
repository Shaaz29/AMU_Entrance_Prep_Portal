import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amu_portal.settings')
django.setup()

from prep.models import UserProfile

profile = UserProfile.objects.exclude(photo="").first()
if profile:
    print(f"Profile: {profile.user.username}")
    print(f"Photo field value: {profile.photo.name}")
    try:
        print(f"Photo URL: {profile.photo.url}")
    except Exception as e:
        print(f"URL error: {e}")
else:
    print("No profiles with photos found.")
