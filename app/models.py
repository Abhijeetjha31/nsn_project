
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Work(models.Model):
    LINK_TYPES = [
        ('youtube', 'Youtube'),
        ('instagram', 'Instagram'),
        ('other', 'Other'),
    ]
    link = models.URLField(max_length=255)
    work_type = models.CharField(max_length=10, choices=LINK_TYPES)

class Artist(models.Model):
    name = models.CharField(max_length=255)
    works = models.ManyToManyField(Work)
