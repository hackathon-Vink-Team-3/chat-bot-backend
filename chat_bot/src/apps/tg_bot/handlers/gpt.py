import logging

from telebot import types, TeleBot

from src.apps.chat.models import Dialog, Chat, Message
from src.apps.core import YaGptRequests
from src.apps.users.models import CustomUser
from src.base.utils import log_exceptions, get_model_config

logger = logging.getLogger(__name__)


@log_exceptions(logger)
def gpt_answer(
    message: types.Message,
    bot: TeleBot,
    user: CustomUser,
    chat: Chat,
    dialog: Dialog,
):
    """Запрос к GPT модели."""
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
    gpt_answer_message = YaGptRequests(
        async_request=False,
        config=get_model_config(),
    ).request(
        message=message.text,
        chat_uuid=str(chat.id),
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
