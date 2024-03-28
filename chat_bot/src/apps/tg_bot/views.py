import http

from rest_framework.decorators import api_view
from rest_framework.response import Response
from telebot import types

from src.apps.tg_bot.loader import bot


@api_view(["POST"])
def web_hook_tg_bot(request) -> Response:
    """Эндпоинт для вебхука."""
    try:
        update = types.Update.de_json(request.data)
        bot.process_new_updates([update])
    except (TypeError, KeyError):
        return Response(status=http.HTTPStatus.BAD_REQUEST)
    return Response(status=http.HTTPStatus.OK)
