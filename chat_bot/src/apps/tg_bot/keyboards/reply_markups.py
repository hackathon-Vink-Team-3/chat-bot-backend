from telebot.types import ReplyKeyboardMarkup, KeyboardButton

pq = (
    "Как оформить заказ?",
    "Какие сроки доставки?",
    "Минимальная сумма заказа?",
    "Что подойдет для оклейки машины?",
    "Почему я?",
)
# TODO Изменить список популярных вопросов


def popular_q_markup(
    popular_questions: tuple[str] = pq,
) -> ReplyKeyboardMarkup:
    """Клавиатура с популярными вопросами."""
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Ответит Vink...",
        row_width=2,
    )
    markup.add(*[KeyboardButton(i) for i in popular_questions])

    return markup
