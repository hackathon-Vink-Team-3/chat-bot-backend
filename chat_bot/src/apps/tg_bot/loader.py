import atexit
import time

from django.conf import settings
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import BotCommandScopeDefault, BotCommand

from src.apps.tg_bot.handlers import start_help, gpt

# Количество потоков можно будет отрегулировать
bot = TeleBot(token=settings.BOT_TOKEN, parse_mode="HTML", num_threads=10)


def register_handlers() -> None:
    """Зарегистрировать обработчики."""
    bot.register_message_handler(
        start_help.command_start_handler,
        commands=["start"],
        pass_bot=True,
    )
    bot.register_message_handler(
        start_help.command_help_handler,
        commands=["help"],
        pass_bot=True,
    )
    # Регистрируем всегда последним
    bot.register_message_handler(
        gpt.gpt_answer,
        func=lambda message: True,
        pass_bot=True,
    )


def set_default_commands(commands: list[tuple[str, str]]) -> None:
    """Добавить команды бота и кнопку меню."""
    commands = [BotCommand(command=c, description=d) for c, d in commands]
    bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault(),
    )


@atexit.register
def on_shutdown() -> None:
    """Удалить команды бота и кнопку меню."""
    bot.remove_webhook()
    bot.delete_my_commands(scope=BotCommandScopeDefault())
    try:
        bot.close()
    except ApiTelegramException:
        pass


def on_startup() -> None:
    """Подготовка бота перед запуском."""
    set_default_commands(settings.BOT_COMMANDS)
    register_handlers()
    bot.remove_webhook()
    time.sleep(0.5)
    bot.set_webhook(
        url=settings.WEBHOOK_URL,
        drop_pending_updates=True,
        secret_token=settings.WEBHOOK_SECRET,
    )
