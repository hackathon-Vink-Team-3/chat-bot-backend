from telebot import types, TeleBot

from src.apps.tg_bot.keyboards import BotKeyboards


def feedback_gateway(message: types.Message, bot: TeleBot):
    """Обработчик входа в состояние оценки бота."""
    bot.send_message(
        chat_id=message.from_user.id,
        text="Пожалуйста оцените работу сервиса от 1 до 10.",
        reply_markup=BotKeyboards.feedback_inline_markup(),
    )
