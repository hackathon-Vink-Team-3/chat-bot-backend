from telebot.callback_data import CallbackData
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


class BotKeyboards:
    """Инлайн и Реплай клавиатуры."""

    FEEDBACK_CALLBACK_DATA = CallbackData("value", prefix="feedback")
    popular_questions = (
        "Как оформить заказ?",
        "Какие сроки доставки?",
        "Минимальная сумма заказа?",
        "Что подойдет для оклейки машины?",
        "Почему я?",
    )
    assessments = (
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

    @classmethod
    def feedback_inline_markup(
        cls,
        assessments: tuple[tuple] = assessments,
    ) -> InlineKeyboardMarkup:
        """Клавиатура для оценки работы бота."""
        markup = InlineKeyboardMarkup(row_width=5)
        markup.add(
            *[
                InlineKeyboardButton(
                    text=a[0],
                    callback_data=cls.FEEDBACK_CALLBACK_DATA.new(value=a[1]),
                )
                for a in assessments
            ]
        )
        return markup

    @classmethod
    def popular_questions_reply_markup(
        cls,
        popular_questions: tuple[str] = popular_questions,
    ) -> ReplyKeyboardMarkup:
        """Клавиатура с популярными вопросами."""
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            input_field_placeholder="Ответит Vink...",
            row_width=2,
        )
        markup.add(*[KeyboardButton(i) for i in popular_questions])

        return markup
