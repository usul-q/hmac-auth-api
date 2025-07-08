from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    public_key = models.CharField(max_length=64, unique=True, blank=True, null=True)
    private_key = models.CharField(max_length=128, blank=True, null=True)
    secret = models.CharField(max_length=200, blank=True, null=False)