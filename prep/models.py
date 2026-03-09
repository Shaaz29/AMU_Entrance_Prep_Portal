from django.db import models
from django.contrib.auth.models import User


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
    TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice'),
        ('NUM', 'Numerical')
    ]

    mocktest = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    text = models.TextField()

    # MCQ Options
    option_a = models.CharField(max_length=200, blank=True)
    option_b = models.CharField(max_length=200, blank=True)
    option_c = models.CharField(max_length=200, blank=True)
    option_d = models.CharField(max_length=200, blank=True)

    correct_answer = models.CharField(max_length=100)

    explanation = models.TextField(blank=True)
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)

    def __str__(self):
        return f"Q{self.id} - {self.mocktest.course.name}"


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    mocktest = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.mocktest} - {self.score}"