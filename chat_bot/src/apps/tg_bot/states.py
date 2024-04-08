from telebot.handler_backends import StatesGroup, State


class AssessmentsStateGroup(StatesGroup):
    """Группа состояний для получения оценки."""

    get_assessment = State()
