import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Chat(models.Model):
    """Модель чат."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    is_open = models.BooleanField(
        default=True,
        verbose_name="Чат открыт.",
    )
    is_support_connected = models.BooleanField(
        default=False,
        verbose_name="Поддержка подключена.",
    )
    created_date = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name="Дата создания.",
    )
    user_id = models.ForeignKey(
        to=User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="chats",
        verbose_name="Пользователь.",
    )


class Message(models.Model):
    """Модель сообщения."""

    pass
