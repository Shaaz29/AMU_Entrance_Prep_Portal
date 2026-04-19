from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MockTest(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='mocktests')
    year = models.IntegerField()
    duration = models.IntegerField(help_text="Duration in minutes")

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.course.name} Mock Test {self.year}"


class Question(models.Model):
    mocktest = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=3, default='MCQ', editable=False)
    text = models.TextField()

    # MCQ Options
    option_a = models.CharField(max_length=200, blank=True)
    option_b = models.CharField(max_length=200, blank=True)
    option_c = models.CharField(max_length=200, blank=True)
    option_d = models.CharField(max_length=200, blank=True)

    correct_answer = models.CharField(max_length=100)

    # Explanation for answer
    explanation = models.TextField(blank=True)


    # Image path (diagram) or comma-separated paths
    image = models.TextField(blank=True, null=True)

    # Explanation image path or comma-separated image paths
    explanation_image = models.TextField(blank=True, null=True)

    @property
    def explanation_image_urls_list(self):
        raw = (self.explanation_image or "").strip()
        if not raw:
            return []
            
        urls = []
        for img in raw.split(','):
            img = img.strip()
            if not img:
                continue
            if img.startswith(("http://", "https://", "/")):
                urls.append(img)
            elif img.startswith("static/"):
                urls.append(f"{settings.STATIC_URL}{img[len('static/'):]}")
            elif img.startswith("media/"):
                urls.append(f"{settings.MEDIA_URL}{img[len('media/'):]}")
            else:
                urls.append(f"{settings.STATIC_URL}{img}")
        return urls

    @property
    def explanation_image_url(self):
        urls = self.explanation_image_urls_list
        return urls[0] if urls else ""
    @property
    def image_urls_list(self):
        raw = (self.image or "").strip()
        if not raw:
            return []
            
        urls = []
        for img in raw.split(','):
            img = img.strip()
            if not img:
                continue
            if img.startswith(("http://", "https://", "/")):
                urls.append(img)
            elif img.startswith("static/"):
                urls.append(f"{settings.STATIC_URL}{img[len('static/'):]}")
            elif img.startswith("media/"):
                urls.append(f"{settings.MEDIA_URL}{img[len('media/'):]}")
            else:
                urls.append(f"{settings.STATIC_URL}{img}")
        return urls

    @property
    def image_url(self):
        urls = self.image_urls_list
        return urls[0] if urls else ""

    def __str__(self):
        return f"Q{self.id} - {self.mocktest.course.name}"


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    mocktest = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='results')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    performance_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.mocktest} - {self.score}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    photo_position_x = models.PositiveSmallIntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    photo_position_y = models.PositiveSmallIntegerField(
        default=35,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"Profile - {self.user.username}"


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_otps')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        from django.utils import timezone
        diff = timezone.now() - self.created_at
        return diff.total_seconds() > 600

    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp}"
