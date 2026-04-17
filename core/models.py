from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'O‘qituvchi'),
        ('student', 'Talaba')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Test(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=20)
    correct_answer = models.TextField()
    points = models.IntegerField(default=1)


class Result(models.Model):
    score = models.FloatField()
