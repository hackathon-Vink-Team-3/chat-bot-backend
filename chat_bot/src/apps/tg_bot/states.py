from telebot.handler_backends import StatesGroup, State


class AssessmentsStateGroup(StatesGroup):
    get_assessment = State()
