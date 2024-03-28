from telebot.callback_data import CallbackData
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


class BotKeyboards:
    """Инлайн и Реплай клавиатуры."""

    feedback_call_factory = CallbackData("value", prefix="feedback")

    @classmethod
    def feedback_inline_markup(
        cls,
        assessments: tuple[tuple],
    ) -> InlineKeyboardMarkup:
        """Клавиатура для оценки работы бота."""
        markup = InlineKeyboardMarkup(row_width=5)
        markup.add(
            *[
                InlineKeyboardButton(
                    text=a[0],
                    callback_data=cls.feedback_call_factory.new(value=a[1]),
                )
                for a in assessments
            ]
        )
        return markup

    @classmethod
    def popular_questions_reply_markup(
        cls,
        popular_questions: tuple[str],
    ) -> ReplyKeyboardMarkup:
        """Клавиатура с популярными вопросами."""
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            input_field_placeholder="Ответит Vink...",
            row_width=2,
        )
        markup.add(*[KeyboardButton(i) for i in popular_questions])

        return markup

    @classmethod
    def cancel_button(cls):
        button = InlineKeyboardButton(
            text="❌",
            callback_data="cancel",
        )
        return button
