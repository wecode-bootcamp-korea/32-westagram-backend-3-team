from unicodedata import name
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    contact = models.CharField(max_length=300)
    
    class Meta:
        db_table = 'users'