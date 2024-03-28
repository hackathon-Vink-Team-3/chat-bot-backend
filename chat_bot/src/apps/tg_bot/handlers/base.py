import logging

from telebot import types, TeleBot

from src.apps.tg_bot.keyboards import BotKeyboards
from src.apps.tg_bot.templates import StartHelpTemplates
from src.base.utils import log_exceptions

logger = logging.getLogger(__name__)


@log_exceptions(logger)
def command_start_handler(message: types.Message, bot: TeleBot):
    """Отправить приветствие."""
    popular_questions = StartHelpTemplates.get_popular_questions()
    bot.send_message(
        chat_id=message.from_user.id,
        text=StartHelpTemplates.START_MESSAGE,
        reply_markup=BotKeyboards.popular_questions_reply_markup(
            popular_questions
        ),
    )
    logger.debug(f"Telegram bot send start message to {message.from_user.id}")


@log_exceptions(logger)
def command_help_handler(message: types.Message, bot: TeleBot):
    """Отправить инструкцию по использованию."""
    bot.send_message(
        chat_id=message.from_user.id,
        text=StartHelpTemplates.HELP_MESSAGE,
    )
    logger.debug(f"Telegram bot send help message to {message.from_user.id}")


def not_text_handler(message: types.Message, bot: TeleBot):
    """Ответ на все сообщения тип которых не текст."""
    bot.send_message(chat_id=message.from_user.id, text="Я вас не понял.")


def cancel_any_state(call: types.CallbackQuery, bot: TeleBot):
    """Сброс любого состояния."""
    print(call.inline_message_id)
    bot.delete_state(call.from_user.id, call.from_user.id)
    bot.send_message(chat_id=call.from_user.id, text="Состояние сброшено.")
