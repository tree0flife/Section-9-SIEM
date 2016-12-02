from django.db import models

# Create your models here.
class Bash_History(models.Model):
    user = models.CharField(max_length=30)
    command = models.CharField(max_length=20)