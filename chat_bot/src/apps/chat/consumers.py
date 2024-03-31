import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """Реализация функциональности чата."""

    serializer_class = None
    queryset = None

    async def get_chat_uuid(self):
        """Получить чат UUID"""
        path_uuid = self.scope["url_route"]["kwargs"]["chat_uuid"]
        pass

    def get_serializer(self):
        """Получить сериализатор."""
        return self.serializer_class

    async def save_message(self, message: dict):
        """Сохранить сообщение."""
        pass

    async def connect(self):
        """Установить соединение."""
        chat_uuid = await self.get_chat_uuid()
        if not chat_uuid:
            await self.close()
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        """Получить сообщения."""
        text_data_json = json.loads(text_data)
        pass  # TODO Вернуть сохраненное сообщение, сохранить вернуть ответ от GPT
