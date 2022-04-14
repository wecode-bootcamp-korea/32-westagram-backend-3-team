from django.db import models

# Create your models here.

class User(models.Model):
    name  = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    Cellphone = models.CharField(max_length=11))

    class Meta:
        db_table = 'users'
