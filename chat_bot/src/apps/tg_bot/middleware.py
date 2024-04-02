import logging

from telebot import BaseMiddleware, TeleBot, CancelUpdate, types

from src.apps.chat.models import Chat, Dialog
from src.apps.tg_bot.keyboards import BotKeyboards
from src.apps.tg_bot.templates import BaseTemplates
from src.apps.users.models import CustomUser
from src.base.utils import log_exceptions, generate_random_password

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__()
        self.update_types = ["message"]
        self.bot = bot

    def pre_process(self, message: types.Message, data):
        user_exists = CustomUser.objects.filter(
            telegram_id=message.from_user.id
        ).exists()
        if message.text in ["/start", "/help"]:
            return
        if not user_exists:
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

            user: CustomUser | None = CustomUser.objects.filter(
                phone_number=phone_number
            ).first()
            if user:
                user.telegram_id = message.from_user.id
                user.save()
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text="Ваш телеграм аккаунт успешно привязан.",
                    reply_markup=types.ReplyKeyboardRemove(),
                )
                logger.info("The user linked the telegram account.")
            else:
                password = generate_random_password()
                user = CustomUser.objects.create_user(
                    username=message.from_user.username,
                    phone_number=phone_number,
                    password=password,
                    telegram_id=message.from_user.id,
                )
                self.create_chat_and_dialog(user=user)
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text="✅ Вы успешно зарегистрированы\.\n"
                    f"Ваш временный пароль для входа на сайт: ||{password}||",
                    reply_markup=types.ReplyKeyboardRemove(),
                    parse_mode="MarkdownV2",
                )
            logger.info("The user is registered.")
            self.bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.id,
            )
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text="❌ Регистрация отменена.",
                reply_markup=types.ReplyKeyboardRemove(),
            )
            return CancelUpdate()

    def create_chat_and_dialog(self, user: CustomUser):
        """Создать диалог и чат."""
        chat = Chat.objects.filter(user=user).first()
        if not chat:
            chat = Chat.objects.create(user=user)
            Dialog.objects.create(chat=chat)
        elif chat and not Dialog.objects.filter(chat=chat, is_open=True):
            Dialog.objects.create(chat=chat)


class ChatDialogMiddleware(BaseMiddleware):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__()
        self.update_types = ["message", "callback_query"]
        self.bot = bot

    @log_exceptions(logger)
    def pre_process(self, upd: types.Message | types.CallbackQuery, data):
        if isinstance(upd, types.Message) and upd.text in [
            ["/start", "/help"]
        ]:
            return
        if isinstance(upd, types.CallbackQuery) and upd.data in ["cancel"]:
            return
        user_id = upd.from_user.id
        user = CustomUser.objects.filter(telegram_id=user_id).first()
        if not user:
            return
        chat = Chat.objects.filter(user=user).first()
        dialog = Dialog.objects.filter(chat=chat, is_open=True).first()
        if not dialog:
            dialog = Dialog.objects.create(chat=chat)
        data["user"], data["chat"], data["dialog"] = user, chat, dialog
