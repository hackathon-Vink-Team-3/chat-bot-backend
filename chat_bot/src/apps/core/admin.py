from django.contrib import admin
from django.contrib.auth.models import Group

from src.apps.core.models import YaGptSettings


@admin.register(YaGptSettings)
class YaGptSettingsAdmin(admin.ModelAdmin):
    """Админ панель для настроек модели."""

    list_display = (
        "id",
        "title",
        "catalog_id",
        "temperature",
        "base_prompt_text",
        "base_error_answer",
        "now_active",
        "context_ttl_seconds",
        "max_tokens",
    )
    list_display_links = "id", "title"
    list_editable = "temperature", "now_active"
    search_fields = "title", "employee__last_name"
    search_help_text = "Поиск по названию."


admin.site.unregister(Group)
