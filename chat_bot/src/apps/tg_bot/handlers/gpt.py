# Тут будем реализовывать подключение к GPT
import logging

from telebot import types, TeleBot

from src.base.utils import log_exceptions

logger = logging.getLogger(__name__)


@log_exceptions(logger)
def gpt_answer(message: types.Message, bot: TeleBot):
    """Заглушка."""
    bot.send_message(
        chat_id=message.from_user.id,
        text="Ответ на любой вопрос.",
    )

    # TODO как хранить контекст? Как сбрасывать контекст(по кнопке?)?
