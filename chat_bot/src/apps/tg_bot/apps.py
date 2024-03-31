from django.apps import AppConfig

from src.apps.tg_bot.loader import on_startup


class TGBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.tg_bot"

    def ready(self) -> None:
        """Подготовить бота перед запуском приложения."""
        on_startup()
