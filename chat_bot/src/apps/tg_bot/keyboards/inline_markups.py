from telebot.callback_data import CallbackData
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

assessments = (
    ("1️⃣", "1"),
    ("2️⃣", "2"),
    ("3️⃣", "3"),
    ("4️⃣", "4"),
    ("5️⃣", "5"),
)
feedback_callback_data = CallbackData("value", prefix="feedback")


def feedback_markup():
    """Клавиатура для оценки работы бота."""
    markup = InlineKeyboardMarkup(row_width=5)
    markup.add(
        *[
            InlineKeyboardButton(text=a[0], callback_data=a[1])
            for a in assessments
        ]
    )
    return markup
