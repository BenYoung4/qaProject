from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_helpdesk = models.BooleanField(default=False)
    email = models.EmailField(unique=True)