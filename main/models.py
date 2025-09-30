from django.db import models

# Create your models here.
class User(models.Model):
    """
    A simple, custom user model for storing login and signup data,
    completely separate from Django's built-in auth system.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Stores the hashed password

    def __str__(self):
        return self.email