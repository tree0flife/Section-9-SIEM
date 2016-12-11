from django.db import models

# Create your models here.
class Bash_History(models.Model):
    username = models.CharField(max_length=30)
    command = models.CharField(max_length=60)
    time= models.CharField(max_length=20)

class Network(models.Model):
    username = models.CharField(max_length=30)
    ip = models.CharField(max_length=15)
    time= models.CharField(max_length=20)

