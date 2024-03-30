from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """
    Модель пользователя.
    Добавлен номер телефона, так как регистрация на основном сайте
    реализована через него.
    Переопределено поле username что бы сделать его необязательным.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            "unique": "Пользователь с таким username уже существует.",
        },
        blank=True,
        null=True,
        verbose_name="username",
    )
    phone_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\+?7\d{10}$",
                message="Номер телефона должен быть в формате '+79991234567'.",
            )
        ],
        verbose_name="Номер телефона",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
