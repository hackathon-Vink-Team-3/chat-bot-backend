from telebot import types, TeleBot

from src.apps.tg_bot.keyboards import BotKeyboards


def command_start_handler(message: types.Message, bot: TeleBot):
    """Отправить приветствие."""
    bot.send_message(
        chat_id=message.from_user.id,
        text="Приветствие",
        reply_markup=BotKeyboards.popular_questions_reply_markup(),
    )


def command_help_handler(message: types.Message, bot: TeleBot):
    """Отправить инструкцию по использованию."""
    bot.send_message(
        chat_id=message.from_user.id,
        text="Инструкция.",
    )
