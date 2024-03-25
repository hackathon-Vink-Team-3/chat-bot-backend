from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Модель пользователя.
    """
    pass


class Role(models.Model):
    """
    Модель ролей.
    """
    pass
