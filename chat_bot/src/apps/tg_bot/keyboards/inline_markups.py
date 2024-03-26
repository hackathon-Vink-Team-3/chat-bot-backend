from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def feedback_markup():
    """Клавиатура для оценки работы бота."""
    markup = InlineKeyboardMarkup(row_width=2)
    button = InlineKeyboardButton(text=..., callback_data=...)
    ...
    return markup
