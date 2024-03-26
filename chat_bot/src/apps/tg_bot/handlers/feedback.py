from telebot import types, TeleBot

from src.apps.tg_bot.keyboards.inline_markups import feedback_markup


def feedback_gateway(message: types.Message, bot: TeleBot):
    """Обработчик входа в состояние оценки бота."""
    bot.send_message(
        chat_id=message.from_user.id,
        text="Пожалуйста оцените работу сервиса от 1 до 5.",
        reply_markup=feedback_markup(),
    )
