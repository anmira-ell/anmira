from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=20, choices=[
        ("male", "Male"), ("female", "Female")
    ])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"