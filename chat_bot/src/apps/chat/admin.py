from django.contrib import admin

from src.apps.chat.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Админ панель для сообщений."""

    list_per_page = 20
    list_max_show_all = 40

    list_display = (
        "id",
        "text",
        "sender_type",
        "created_date",
        "chat",
        "dialog",
        "user",
    )
    list_display_links = ("id",)
