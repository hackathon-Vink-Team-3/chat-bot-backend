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
        cls, colored_stars: int = 0
    ) -> InlineKeyboardMarkup:
        """Клавиатура для оценки работы бота."""
        if not colored_stars:
            stars = [(str(i), i) for i in range(1, 11)]
            # Оставил вариант только со звездами что бы не потерять.
            # stars = [("☆", i) for i in range(1, 11)]
        else:
            stars = [
                ("⭐️" if i != 10 else "🌟", i)
                for i in range(1, colored_stars + 1)
            ] + [(str(i), i) for i in range(colored_stars + 1, 11)]
        markup = InlineKeyboardMarkup(row_width=5)
        markup.row(
            *[
                InlineKeyboardButton(
                    text=a[0],
                    callback_data=cls.feedback_call_factory.new(value=a[1]),
                )
                for a in stars
            ]
        )
        if colored_stars:
            markup.row(cls.send_button("send_assessment"))
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
    def get_contact_phone(cls):
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
        )
        button = KeyboardButton(
            "📲Отправить номер телефона.",
            request_contact=True,
        )
        markup.add(button)
        return markup

    @classmethod
    def cancel_button(cls):
        """Кнопка отмена."""
        button = InlineKeyboardButton(
            text="❌",
            callback_data="cancel",
        )
        return button

    @classmethod
    def send_button(cls, callback_data):
        """Кнопка отправить."""
        button = InlineKeyboardButton(
            text="Отправить", callback_data=callback_data
        )
        return button
