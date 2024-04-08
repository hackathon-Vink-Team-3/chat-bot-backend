from django.db import models


class YaGptSettings(models.Model):
    """Модель настроек YandexGPT."""

    title = models.CharField(
        max_length=32,
        verbose_name="Название",
        unique=True,
    )
    catalog_id = models.CharField(
        max_length=32,
        verbose_name="Идентификатор каталога.",
    )
    temperature = models.FloatField(
        verbose_name="Температура",
        help_text="Чем выше значение этого параметра, тем более креативными "
        "и случайными будут ответы модели. Принимает значения "
        "от 0 (включительно) до 1 (включительно).",
    )
    base_prompt_text = models.TextField(
        verbose_name="Cистемное сообщение.",
        help_text="Позволяет задать контекст запроса и "
        "определить поведение модели.",
    )
    base_error_answer = models.TextField(
        verbose_name="Сообщение об ошибке.",
        help_text="Это сообщение будет отправлено пользователю "
        "при отсутствии ответа от модели.",
    )
    now_active = models.BooleanField(
        verbose_name="Активна.",
        help_text="Активной может быть только одна запись настроек.",
    )
    context_ttl_seconds = models.PositiveSmallIntegerField(
        verbose_name="Время хранения контекста.",
        help_text="Количество секунд для хранения контекста в "
        "неактивном диалоге.",
    )
    max_tokens = models.PositiveSmallIntegerField(
        verbose_name="Символов в ответе.",
        help_text="Максимальное количество символов в ответе модели.",
    )

    class Meta:
        verbose_name = "Настройки модели"
        verbose_name_plural = "Настройки модели"
        constraints = [
            models.UniqueConstraint(
                fields=("now_active",),
                condition=models.Q(now_active=True),
                name="unique_now_active",
            ),
        ]

    def __str__(self):
        return self.title
