from telebot import types, TeleBot


def command_start_handler(message: types.Message, bot: TeleBot):
    """Отправить приветствие."""
    bot.send_message(
        chat_id=message.from_user.id,
        text="Приветствие",
    )


def command_help_handler(message: types.Message, bot: TeleBot):
    """Отправить инструкцию по использованию."""
    bot.send_message(
        chat_id=message.from_user.id,
        text="Инструкция.",
    )
