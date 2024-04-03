import json
import logging
from json import JSONDecodeError

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from src.apps.chat.models import Message, Dialog
from src.apps.chat.serializers import MessageSerializer

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """Реализация функциональности чата."""

    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_path_kwargs(self) -> tuple[str, str]:
        """Получить параметры пути."""
        chat_uuid: str = self.scope["url_route"]["kwargs"].get("chat_uuid")
        dialog_id: str = self.scope["url_route"]["kwargs"].get("dialog_id")
        return chat_uuid, dialog_id

    async def check_path(self) -> bool:
        """Проверить существует ли открытый диалог по параметрам пути."""
        chat_uuid, dialog_id = self.get_path_kwargs()
        check: bool = await Dialog.objects.filter(
            id=dialog_id,
            chat_id=chat_uuid,
            is_open=True,
        ).aexists()
        return check

    async def get_gpt_answer(self, message: str) -> str:
        """Получить ответ от GPT модели."""

        # TODO Отправляем на обработку модели(message)

        gpt_answer = "VINK скрывают что я бот, помогите!"
        logger.info("The response from GPT has been received.")
        return gpt_answer

    async def send_error(self, error_message) -> None:
        """Отправить сообщение об ошибке."""
        await self.send(text_data=json.dumps({"error": error_message}))

    async def parse_received_data(self, text_data: str) -> str | None:
        """Обработать полученные данные."""
        try:
            parsed_data: dict = json.loads(text_data)
        except JSONDecodeError:
            return await self.send_error("Json parse failed.")
        message_text: str | None = parsed_data.get("text")
        if not message_text:
            return await self.send_error("The key 'text' is missing.")
        logger.info("The received data has been processed.")
        return message_text

    async def save_message(
        self, message_text: str, sender_type
    ) -> tuple[dict, str] | str | None:
        """Сохранить сообщение."""
        chat_uuid, dialog_id = self.get_path_kwargs()
        data = dict(
            text=message_text,
            sender_type=sender_type,
            chat_id=chat_uuid,
            dialog_id=dialog_id,
        )
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return await self.send_error("Serialize failed.")
        await sync_to_async(serializer.save)(**data)
        logger.info(f"The message has been saved. Sender type: {sender_type}")
        if sender_type == "user":
            return serializer.data["text"], json.dumps(serializer.data)
        return json.dumps(serializer.data)

    async def connect(self) -> None:
        """Установить соединение."""
        check = await self.check_path()
        if not check:
            await self.close()
            logger.info("WS connection denied.")
        await self.accept()
        logger.info("WS connected.")

    async def receive(self, text_data=None, bytes_data=None) -> None:
        """Получить и отправить сообщения."""
        message_text: str = await self.parse_received_data(text_data)
        message_to_gpt, message = await self.save_message(
            message_text,
            sender_type="user",
        )
        if message_to_gpt and message:
            await self.send(message)
            logger.info("The saved message has been sent.")
            gpt_answer = await self.get_gpt_answer(message_to_gpt)
            saved_gpt_answer: str = await self.save_message(
                gpt_answer, sender_type="bot"
            )
            if saved_gpt_answer:
                await self.send(saved_gpt_answer)
                logger.info("The saved bot answer has been sent.")
