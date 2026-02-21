from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MockTest(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.course.name} {self.year}"


class Question(models.Model):
    TYPE_CHOICES = [
        ('MCQ', 'MCQ'),
        ('NUM', 'Numerical')
    ]

    mocktest = models.ForeignKey(MockTest, on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    text = models.TextField()

    option_a = models.CharField(max_length=200, blank=True)
    option_b = models.CharField(max_length=200, blank=True)
    option_c = models.CharField(max_length=200, blank=True)
    option_d = models.CharField(max_length=200, blank=True)

    correct_answer = models.CharField(max_length=100)
    explanation = models.TextField(blank=True)
    image = models.ImageField(upload_to='question_images/', blank=True)


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mocktest = models.ForeignKey(MockTest, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)