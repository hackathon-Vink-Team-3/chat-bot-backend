from django.urls import re_path

from src.apps.chat import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<chat_uuid>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
