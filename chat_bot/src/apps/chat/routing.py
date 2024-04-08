from django.urls import re_path

from src.apps.chat import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/chat/(?P<chat_uuid>[0-9a-f\-]+)/dialog/((?P<dialog_id>\w+)/)$",
        consumers.ChatConsumer.as_asgi(),
    ),
    re_path(r".*", consumers.ChatConsumer.as_asgi()),
]
