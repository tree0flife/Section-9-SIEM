from django.db import models

# Create your models here.
class Bash_History(models.Model):
    client = models.CharField(max_length=30)
    command = models.CharField(max_length=20)