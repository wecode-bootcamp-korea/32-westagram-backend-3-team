from django.db import models

# Create your models here.

class User(models.Model):
   user_name  = models.CharField(max_length=20)
   user_email = models.CharField(unique=True)
   user_password = models.CharField(max_length=100)
   user_phone_number = models.CharField(max_length=30)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
