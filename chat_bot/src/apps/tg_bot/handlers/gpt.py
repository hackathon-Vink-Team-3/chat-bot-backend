# Тут будем реализовывать подключение к GPT

from telebot import types, TeleBot


def gpt_answer(message: types.Message, bot: TeleBot):
    """Заглушка."""
    bot.send_message(
        chat_id=message.from_user.id,
        text="Ответ на любой вопрос.",
    )
