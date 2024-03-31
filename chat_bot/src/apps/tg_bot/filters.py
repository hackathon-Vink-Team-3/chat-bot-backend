from telebot import AdvancedCustomFilter, types
from telebot.callback_data import CallbackDataFilter


class CustomCallbackFilter(AdvancedCustomFilter):
    """Фильтр для коллбеков."""

    key = "config"

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)
