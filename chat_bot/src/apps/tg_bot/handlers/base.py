import logging

from telebot import types, TeleBot

from src.apps.tg_bot.keyboards import BotKeyboards
from src.apps.tg_bot.templates import BaseTemplates
from src.base.utils import log_exceptions

logger = logging.getLogger(__name__)


@log_exceptions(logger)
def command_start_handler(message: types.Message, bot: TeleBot):
    """Отправить приветствие."""
    popular_questions = BaseTemplates.get_popular_questions()
    bot.send_message(
        chat_id=message.chat.id,
        text=BaseTemplates.START_MESSAGE,
        reply_markup=BotKeyboards.popular_questions_reply_markup(
            popular_questions
        ),
    )
    logger.debug(f"Telegram bot send start message to {message.from_user.id}")


@log_exceptions(logger)
def command_help_handler(message: types.Message, bot: TeleBot):
    """Отправить инструкцию по использованию."""
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot.send_message(
        chat_id=message.chat.id,
        text=BaseTemplates.HELP_MESSAGE,
    )
    logger.debug(f"Telegram bot send help message to {message.from_user.id}")


@log_exceptions(logger)
def not_text_handler(message: types.Message, bot: TeleBot):
    """Ответ на все сообщения тип которых не текст."""
    bot.send_message(
        chat_id=message.chat.id,
        text=BaseTemplates.NOT_TEXT_MESSAGE,
    )
    logger.debug(
        f"Telegram bot send not text type message to {message.from_user.id}"
    )


@log_exceptions(logger)
def cancel_any_state(call: types.CallbackQuery | types.Message, bot: TeleBot):
    """Сброс любого состояния."""
    bot.delete_state(user_id=call.from_user.id, chat_id=call.from_user.id)
    if isinstance(call, types.Message):
        bot.send_message(chat_id=call.chat.id, text=BaseTemplates.STATE_CLEAR)
        bot.delete_message(chat_id=call.chat.id, message_id=call.id)
    else:
        bot.answer_callback_query(call.id, text=BaseTemplates.CANCEL_CALLBACK)
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
        )
