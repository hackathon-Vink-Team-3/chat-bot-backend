import sys

from django.core.management import BaseCommand
from environs import Env

from src.apps.core.models import YaGptSettings

env = Env()


class Command(BaseCommand):
    """Команда для загрузки базовых настроек модели в БД."""

    def handle(self, *args, **options):
        if not self.check_settings_model():
            sys.stdout.write(
                "There are already entries in the model settings table.\n"
            )
            sys.exit()
        YaGptSettings.objects.create(
            title="auto-base",
            catalog_id=env.str("YA_CATALOG_ID"),
            temperature=env.float("MODEL_TEMPERATURE"),
            now_active=True,
            context_ttl_seconds=1200,
            max_tokens=1500,
            base_error_answer=env.str("BASE_ERROR_ANSWER"),
            base_prompt_text=env.str("BASE_PROMPT_TEXT"),
        )
        sys.stdout.write("The settings have been successfully added.\n")

    def check_settings_model(self):
        settings = YaGptSettings.objects.all()
        if settings:
            return False
        return True
