import logging
from time import sleep

from telebot import types, TeleBot

from src.apps.chat.models import Dialog, Chat, Message
from src.apps.users.models import CustomUser
from src.base.utils import log_exceptions

logger = logging.getLogger(__name__)


@log_exceptions(logger)
def gpt_answer(
    message: types.Message,
    bot: TeleBot,
    user: CustomUser,
    chat: Chat,
    dialog: Dialog,
):
    """Заглушка."""
    wait_message = bot.send_message(
        chat_id=message.from_user.id, text="Надо немного подумать...."
    )
    Message.objects.create(
        chat=chat,
        dialog=dialog,
        user=user,
        text=message.text,
        sender_type="user",
    )
    logger.debug("Telegram bot saved message. Sender type: user")
    bot.send_chat_action(chat_id=message.chat.id, action="typing", timeout=3)

    sleep(3)  # TODO УБРАТЬ ПОСЛЕ ПОДКЛЮЧЕНИЯ GPT!
    gpt_answer_message = (
        "Тут будет очень точный ответ, который точно вам поможет."
    )

    Message.objects.create(
        chat=chat,
        dialog=dialog,
        text=gpt_answer_message,
        sender_type="bot",
    )
    logger.debug("Telegram bot saved message. Sender type: bot")
    bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=wait_message.id,
        text=gpt_answer_message,
    )

    # TODO как хранить контекст? Как сбрасывать контекст(по кнопке?)?
