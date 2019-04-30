from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Instructor(models.Model):
    # make a foreign key to Users table here

    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    self_intro = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    thumb = models.ImageField(default='default.png', blank=True)

    def __str__(self):
        return self.username
