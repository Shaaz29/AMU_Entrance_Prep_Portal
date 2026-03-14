import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update a superuser from environment variables."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Skipping superuser setup. Set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD."
                )
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        updated = False

        if not user.is_staff:
            user.is_staff = True
            updated = True

        if not user.is_superuser:
            user.is_superuser = True
            updated = True

        if email and user.email != email:
            user.email = email
            updated = True

        # Keep password in sync with current deployment env secret.
        if not user.check_password(password):
            user.set_password(password)
            updated = True

        if created or updated:
            user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created superuser: {username}"))
        elif updated:
            self.stdout.write(self.style.SUCCESS(f"Updated superuser: {username}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser already up to date: {username}"))
