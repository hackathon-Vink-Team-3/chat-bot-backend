import logging

from telebot import BaseMiddleware, TeleBot, CancelUpdate, types

from src.apps.tg_bot.keyboards import BotKeyboards
from src.apps.tg_bot.templates import BaseTemplates
from src.base.utils import log_exceptions

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__()
        self.update_types = ["message"]
        self.bot = bot

    def pre_process(self, message, data):
        user = None

        # TODO добавить запрос в базу на получение юзера.

        if message.text in ["/start", "/help", "/registration"]:
            return
        if not user:
            self.registration_gateway(message)
            logger.debug("Update from an unregistered user has been rejected.")
            return CancelUpdate()

    @log_exceptions(logger)
    def registration_gateway(self, message: types.Message):
        contact_message = self.bot.send_message(
            chat_id=message.chat.id,
            text=BaseTemplates.SEND_NUMBER,
            reply_markup=BotKeyboards.get_contact_phone(),
        )
        self.bot.register_next_step_handler(contact_message, self.create_user)

    @log_exceptions(logger)
    def create_user(self, message: types.Message):
        if message.contact:
            phone_number = message.contact.phone_number

            # TODO добавить сохранение пользователя в БД

            self.bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.id,
            )
            self.bot.send_message(
                chat_id=message.chat.id,
                text="✅ Вы успешно зарегистрированы.",
                reply_markup=types.ReplyKeyboardRemove(),
            )
            logger.info("The user is registered.")
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text="❌ Регистрация отменена.",
                reply_markup=types.ReplyKeyboardRemove(),
            )
            return CancelUpdate()
