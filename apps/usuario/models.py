from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    image = models.ImageField(upload_to='users', null=True, blank=True)
