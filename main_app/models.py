from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    genre= models.CharField(max_length=100)
    summary = models.TextField(max_length=250)
    release = models.IntegerField()

    def __str__(self):
      return self.title
