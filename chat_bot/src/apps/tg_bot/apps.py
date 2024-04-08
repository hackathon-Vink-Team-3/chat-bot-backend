from django.apps import AppConfig


class TGBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.tg_bot"

    def ready(self):
        import os
        from src.apps.tg_bot.loader import on_startup

        if os.environ.get("RUN_MAIN"):
            on_startup()
