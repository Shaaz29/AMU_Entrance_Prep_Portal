import os
import django
import traceback

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amu_portal.settings")
# FORCE DEBUG=False
os.environ['DEBUG'] = 'False'
os.environ['DATABASE_URL'] = f"sqlite:///c:/Users/ahmad/OneDrive/Desktop/AMU_ Entrance_Portal/db.sqlite3"

django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS.append('127.0.0.1')
settings.ALLOWED_HOSTS.append('localhost')

from django.core.signals import got_request_exception
def handle_exc(sender, request, **kwargs):
    print("GOT EXCEPTION DURING REQUEST:")
    traceback.print_exc()

got_request_exception.connect(handle_exc)

from django.test import Client
c = Client(raise_request_exception=False)

def check_url(url):
    print(f"Checking {url} with DEBUG=False")
    try:
        r = c.get(url, SERVER_NAME='127.0.0.1')
        print(f"  {url} -> {r.status_code}")
    except Exception as e:
        traceback.print_exc()

check_url('/')
