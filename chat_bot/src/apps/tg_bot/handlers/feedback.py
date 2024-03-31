import logging

from telebot import types, TeleBot

from src.apps.tg_bot.keyboards import BotKeyboards
from src.apps.tg_bot.states import AssessmentsStateGroup
from src.apps.tg_bot.templates import FeedbackTemplates
from src.base.utils import log_exceptions

logger = logging.getLogger(__name__)


@log_exceptions(logger)
def feedback_gateway(message: types.Message, bot: TeleBot):
    """Обработчик входа в состояние оценки бота."""
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    bot.send_message(
        chat_id=message.from_user.id,
        text=FeedbackTemplates.GATEWAY_MESSAGE,
        reply_markup=BotKeyboards.feedback_inline_markup().add(
            BotKeyboards.cancel_button()
        ),
    )
    bot.set_state(
        user_id=user_id,
        state=AssessmentsStateGroup.get_assessment,
        chat_id=chat_id,
    )
    logger.debug(
        f"Telegram Bot send feedback gateway message to {user_id}. "
        f"Set get_assessment state."
    )


@log_exceptions(logger)
def get_assessment_from_user(call: types.CallbackQuery, bot: TeleBot):
    """Получить оценку пользователя."""
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    callback_data: dict = BotKeyboards.feedback_call_factory.parse(call.data)
    assessment_value = callback_data["value"]
    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        data_assessment = data.get("feedback")
    if data_assessment != assessment_value:
        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=BotKeyboards.feedback_inline_markup(
                colored_stars=int(assessment_value)
            ).add(BotKeyboards.cancel_button()),
        )
        with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
            data["feedback"] = assessment_value
    bot.answer_callback_query(
        callback_query_id=call.id,
        text=(
            f"😊 Оценка {assessment_value}"
            if int(assessment_value) > 6
            else f"🙄 Оценка {assessment_value}"
        ),
    )


@log_exceptions(logger)
def save_assessment(call: types.CallbackQuery, bot: TeleBot):
    """Сохранить оценку пользователя."""
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        data_assessment = data.get("feedback")

    # TODO занести в базу оценку от пользователя.

    bot.edit_message_text(
        text=FeedbackTemplates.GET_ASSESSMENT.format(data_assessment),
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=None,
    )
    bot.delete_state(user_id=user_id, chat_id=chat_id)
    bot.answer_callback_query(callback_query_id=call.id, text="✅")
    logger.debug("Telegram Bot delete state, assessment saved.")
