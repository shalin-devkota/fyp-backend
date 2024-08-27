from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=10)
   
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
