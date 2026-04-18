from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')


class Test(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    correct_answer = models.TextField()

    def __str__(self):
        return self.text


class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()
