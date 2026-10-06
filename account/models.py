from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
  class Roles(models.TextChoices):
    SUPERADMIN = 'superadmin', 'مدير'
    ADMIN = 'admin', 'مسؤول كامل'
    STORE = 'store', 'مسؤول المتاجر'
    SALES = 'sales', 'مسؤول المبيعات'
    NONE = 'none'
  role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.NONE)
