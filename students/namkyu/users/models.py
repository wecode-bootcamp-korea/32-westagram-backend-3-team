from platform import release
from pyexpat import model
from tkinter import CASCADE
from turtle import ondrag
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField()
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)

    class Meta:
        db_table = 'users'
