import logging
from time import sleep

from telebot import types, TeleBot

from src.base.utils import log_exceptions

logger = logging.getLogger(__name__)


@log_exceptions(logger)
def gpt_answer(message: types.Message, bot: TeleBot):
    """Заглушка."""
    wait_message = bot.send_message(
        chat_id=message.from_user.id, text="Надо немного подумать...."
    )

    sleep(3)  # TODO УБРАТЬ ПОСЛЕ ПОДКЛЮЧЕНИЯ GPT!

    bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=wait_message.id,
        text="Тут будет очень точный ответ, который точно вам поможет.",
    )

    # TODO как хранить контекст? Как сбрасывать контекст(по кнопке?)?
