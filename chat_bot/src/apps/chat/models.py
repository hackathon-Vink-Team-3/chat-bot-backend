"""
Описание связей моделей приложения Чат.
Модель Chat связана с моделью User один к одному.
Модель Dialog связана с моделью Chat многие к одному.
Модель Message связана с моделями User, Dialog и Chat многие к одному.
"""

import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Chat(models.Model):
    """
    Модель чат.
    Имеет связь один к одному с моделью User.
    Вместо обычного id установлен UUID, используется в куки файлах как
    уникальный идентификатор для неавторизованных пользователей.
    Если пользователь не авторизован, но файлах куки есть UUID чата,
    история чата будет доступна.
    При регистрации нужно привязать чат к созданному объекту пользователя,
    использовав UUID из файлов куки и поле user_id.
    __
    Использовать для вывода истории сообщений.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_date = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name="Дата создания",
    )
    user_id = models.OneToOneField(
        to=User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="chat",
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    def __str__(self):
        return f"Чат UUID {self.id}"


class Dialog(models.Model):
    """
    Модель диалог.
    Промежуточная модель, ее основная цель разбить чат на небольшие диалоги
    для оценки работы бота, аналитики и внутреннего использования.
    Имеет связь многие к одному с моделью Chat.
    Поле is_open говорит о том открыт диалог или закрыт, имеет ограничение -
    у одного пользователя может быть только один открытый диалог.
    Поле is_support_connected должно быть изменено на True при подключении
    к диалогу специалиста службы поддержки.
    """

    is_open = models.BooleanField(
        default=True,
        verbose_name="Чат открыт",
    )
    is_support_connected = models.BooleanField(
        default=False,
        verbose_name="Поддержка подключена",
    )
    assessment = models.PositiveSmallIntegerField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Оценка",
    )
    created_date = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name="Дата создания",
    )
    chat_id = models.ForeignKey(
        to=Chat,
        on_delete=models.CASCADE,
        related_name="dialogs",
        verbose_name="Чат",
    )

    class Meta:
        verbose_name = "Диалог"
        verbose_name_plural = "Диалоги"
        constraints = [
            models.UniqueConstraint(
                fields=("is_open", "chat_id"),
                condition=models.Q(is_open=True),
                name="unique_is_open_for_chat_id",
            ),
        ]

    def __str__(self):
        return f"Диалог id {self.id}"


class Message(models.Model):
    """
    Модель сообщение.
    Имеет связи многие к одному с моделями Chat, Dialog, User.
    Поле sender_type используется для указания типа отправителя, выбор
    реализован через класс SenderType.
    """

    class SenderType(models.TextChoices):
        USER = "user", "user"
        BOT = "bot", "bot"
        SUPPORT = "support", "support"

    text = models.TextField(max_length=2000)
    sender_type = models.CharField(
        choices=SenderType.choices,
        verbose_name="Тип отправителя",
    )
    created_date = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name="Дата создания",
    )
    chat_id = models.ForeignKey(
        to=Chat,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Чат",
    )
    dialog_id = models.ForeignKey(
        to=Dialog,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Диалог",
    )
    user_id = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="messages",
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
