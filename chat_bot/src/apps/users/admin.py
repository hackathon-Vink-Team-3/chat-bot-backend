from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from src.apps.users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Учетные данные",
            {
                "fields": ("username", "password"),
            },
        ),
        (
            "Персональная информация",
            {"fields": ("first_name", "last_name", "email", "phone_number")},
        ),
        (
            "Права доступа",
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
    )
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "phone_number",
    )
    list_display_links = (
        "id",
        "username",
        "first_name",
        "last_name",
    )
    search_fields = ("first_name", "last_name")
