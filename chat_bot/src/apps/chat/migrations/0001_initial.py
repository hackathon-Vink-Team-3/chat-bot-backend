# Generated by Django 4.2.11 on 2024-03-31 22:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="chat",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Чат",
                "verbose_name_plural": "Чаты",
            },
        ),
        migrations.CreateModel(
            name="Dialog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_open",
                    models.BooleanField(
                        default=True, verbose_name="Чат открыт"
                    ),
                ),
                (
                    "is_support_connected",
                    models.BooleanField(
                        default=False, verbose_name="Поддержка подключена"
                    ),
                ),
                (
                    "assessment",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MaxValueValidator(
                                limit_value=10,
                                message="Оценка не может быть больше 10.",
                            ),
                            django.core.validators.MinValueValidator(
                                limit_value=1,
                                message="Не может быть меньше 1.",
                            ),
                        ],
                        verbose_name="Оценка",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dialogs",
                        to="chat.chat",
                        verbose_name="Чат",
                    ),
                ),
            ],
            options={
                "verbose_name": "Диалог",
                "verbose_name_plural": "Диалоги",
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(max_length=2000)),
                (
                    "sender_type",
                    models.CharField(
                        choices=[
                            ("user", "user"),
                            ("bot", "bot"),
                            ("support", "support"),
                        ],
                        max_length=7,
                        verbose_name="Тип отправителя",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="chat.chat",
                        verbose_name="Чат",
                    ),
                ),
                (
                    "dialog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="chat.dialog",
                        verbose_name="Диалог",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="messages",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
                "ordering": ["-created_date"],
            },
        ),
        migrations.AddConstraint(
            model_name="dialog",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_open", True)),
                fields=("is_open", "chat"),
                name="unique_is_open_for_chat_id",
            ),
        ),
    ]