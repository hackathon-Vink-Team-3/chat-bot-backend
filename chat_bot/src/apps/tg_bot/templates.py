class BaseTemplates:
    START_MESSAGE = "Приветствую, я помощник Vink..."
    HELP_MESSAGE = "Сообщение с инструкцией по использованию..."
    NOT_TEXT_MESSAGE = "Я могу ответить только на тестовые сообщения."
    POPULAR_QUESTIONS = (
        "Как оформить заказ?",
        "Какие сроки доставки?",
        "Минимальная сумма заказа?",
        "Что подойдет для оклейки машины?",
        "Почему я?",
    )

    @classmethod
    def get_popular_questions(cls):
        """Получить популярные вопросы."""
        # TODO реализовать получение популярных вопросов.
        # Вопросы должны храниться в бд что бы была возможность их поменять.
        return cls.POPULAR_QUESTIONS


class FeedbackTemplates:
    GATEWAY_MESSAGE = "Поставьте оценку от 1 до 10..."
    ASSESSMENTS = (
        ("1️⃣", "1"),
        ("2️⃣", "2"),
        ("3️⃣", "3"),
        ("4️⃣", "4"),
        ("5️⃣", "5"),
        ("6️⃣", "6"),
        ("7️⃣", "7"),
        ("8️⃣", "8"),
        ("9️⃣", "9"),
        ("🔟", "10"),
    )


class GPTTemplates:
    pass
