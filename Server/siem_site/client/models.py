from django.db import models

class Client(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    token = models.CharField(max_length=20,blank=True)