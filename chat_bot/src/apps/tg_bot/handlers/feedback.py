import logging

from telebot import types, TeleBot

from src.apps.tg_bot.keyboards import BotKeyboards
from src.apps.tg_bot.templates import FeedbackTemplates
from src.base.utils import log_exceptions

logger = logging.getLogger(__name__)


@log_exceptions(logger)
def feedback_gateway(message: types.Message, bot: TeleBot):
    """Обработчик входа в состояние оценки бота."""
    bot.send_message(
        chat_id=message.from_user.id,
        text=FeedbackTemplates.GATEWAY_MESSAGE,
        reply_markup=BotKeyboards.feedback_inline_markup(
            FeedbackTemplates.ASSESSMENTS
        ).add(BotKeyboards.cancel_button()),
    )
    logger.debug(
        f"Telegram Bot send feedback gateway message to {message.from_user.id}"
    )
