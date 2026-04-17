from django.db import models

class Question(models.Model):
    text = models.TextField()
    correct_answer = models.CharField(max_length=200)

class Result(models.Model):
    score = models.IntegerField()
