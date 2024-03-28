import logging

from telebot import types, TeleBot

from src.base.utils import log_exceptions

logger = logging.getLogger(__name__)


@log_exceptions(logger)
def gpt_answer(message: types.Message, bot: TeleBot):
    """Заглушка."""
    bot.send_message(
        chat_id=message.from_user.id,
        text="Тут будет очень точный ответ, который точно вам поможет.",
    )

    # TODO как хранить контекст? Как сбрасывать контекст(по кнопке?)?
