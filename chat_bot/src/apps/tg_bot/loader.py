import atexit
import logging
import time

from django.conf import settings
from telebot import TeleBot, StateMemoryStorage, custom_filters
from telebot.apihelper import ApiTelegramException
from telebot.types import BotCommandScopeDefault, BotCommand

from src.apps.tg_bot import filters
from src.apps.tg_bot.handlers import base, feedback, gpt
from src.apps.tg_bot.keyboards import BotKeyboards
from src.apps.tg_bot.states import AssessmentsStateGroup
from src.apps.tg_bot.templates import BOT_COMMANDS

logger = logging.getLogger(__name__)

state_storage = StateMemoryStorage()

bot = TeleBot(
    token=settings.BOT_TOKEN,
    parse_mode="HTML",
    num_threads=10,  # TODO Количество потоков можно будет отрегулировать
    state_storage=state_storage,
)


def register_handlers() -> None:
    """Зарегистрировать обработчики."""

    bot.register_message_handler(
        base.command_start_handler, commands=["start"], pass_bot=True
    )
    bot.register_message_handler(
        base.command_help_handler, commands=["help"], pass_bot=True
    )
    bot.register_message_handler(
        feedback.feedback_gateway, commands=["feedback"], pass_bot=True
    )
    bot.register_message_handler(
        base.cancel_any_state, commands=["cancel"], pass_bot=True
    )
    bot.register_callback_query_handler(
        feedback.get_assessment_from_user,
        state=AssessmentsStateGroup.get_assessment,
        config=BotKeyboards.feedback_call_factory.filter(),
        pass_bot=True,
        func=None,
    )
    bot.register_callback_query_handler(
        feedback.save_assessment,
        state=AssessmentsStateGroup.get_assessment,
        pass_bot=True,
        func=lambda call: call.data == "send_assessment",
    )
    bot.register_callback_query_handler(
        base.cancel_any_state,
        func=lambda call: call.data == "cancel",
        pass_bot=True,
    )
    # Регистрируем всегда последними
    bot.register_message_handler(
        gpt.gpt_answer,
        func=lambda message: message.content_type == "text",
        pass_bot=True,
    )
    bot.register_message_handler(
        base.not_text_handler, func=lambda message: True, pass_bot=True
    )

    logger.debug("Bot handlers are registered.")


def add_filters():
    """Добавить фильтры."""
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.add_custom_filter(filters.CustomCallbackFilter())


def set_default_commands(commands: list[tuple[str, str]]) -> None:
    """Добавить команды бота и кнопку меню."""
    commands = [BotCommand(command=c, description=d) for c, d in commands]
    bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault(),
    )
    logger.debug("The bot commands are set.")


@atexit.register
def on_shutdown() -> None:
    """Удалить команды бота и кнопку меню."""
    bot.remove_webhook()
    bot.delete_my_commands(scope=BotCommandScopeDefault())
    try:
        bot.close()
    except ApiTelegramException:
        pass
    logger.warning("Telegram bot stopped. Webhook removed, commands deleted.")


def on_startup() -> None:
    """Подготовка бота перед запуском."""
    logger.info("Telegram bot starting...")
    set_default_commands(BOT_COMMANDS)
    register_handlers()
    add_filters()
    bot.remove_webhook()
    time.sleep(0.5)  # Что бы не ловить код 429 при запуске
    bot.set_webhook(
        url=settings.WEBHOOK_URL,
        drop_pending_updates=True,
        secret_token=settings.WEBHOOK_SECRET,
        allowed_updates=["*"],
    )
    logger.warning("Telegram bot started.")
