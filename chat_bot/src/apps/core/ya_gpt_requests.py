import asyncio
import http
import json
import logging

import requests
from aiohttp import (
    ClientSession,
    ClientTimeout,
    ClientResponse as AsyncResponse,
)
from django.conf import settings
from redis import Redis, ConnectionPool
from redis.asyncio import Redis as aRedis, ConnectionPool as AConnectionPool
from requests import Response as SyncResponse, JSONDecodeError

logger = logging.getLogger(__name__)


class YaGptRequests:
    """Запросы к YandexGPT."""

    MODEL_API_KEY: str = f"Api-Key {settings.MODEL_API_KEY}"
    YA_API_URL: str = settings.YA_API_URL
    REDIS_HOST: str = settings.REDIS_HOST

    def __init__(
        self,
        async_request: bool,
        config,
        model_stream: bool = False,
    ):
        self.async_requests = async_request
        self.redis_ttl: int = config.context_ttl_seconds
        self.model_temperature: float = config.temperature
        self.model_max_tokens: int = config.max_tokens
        self.catalog_id: str = config.catalog_id
        self.prompt_text: str = config.base_prompt_text
        self.base_prompt: dict = {"role": "system", "text": self.prompt_text}
        self.base_error_answer: str = config.base_error_answer
        self.model_uri: str = f"gpt://{self.catalog_id}/yandexgpt-lite/latest"
        self.redis_host: str = settings.REDIS_HOST
        self.model_stream: bool = model_stream

    @property
    def redis(self):
        """
        Redis client.
        Зависит от параметра: async_request
        """
        if self.async_requests:
            con_pool = AConnectionPool()
            return aRedis(
                host=self.redis_host,
                connection_pool=con_pool,
            )
        con_pool = ConnectionPool()
        return Redis(host=self.redis_host, connection_pool=con_pool)

    def __headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": self.MODEL_API_KEY,
        }

    def __set_prompt(self, messages: list[dict[str, str]]):
        """Установить prompt."""
        prompt = {
            "modelUri": self.model_uri,
            "completionOptions": {
                "stream": self.model_stream,
                "temperature": self.model_temperature,
                "maxTokens": self.model_max_tokens,
            },
            "messages": [self.base_prompt, *messages],
        }
        return prompt

    def __format_message(self, message: str, role: str) -> dict[str, str]:
        """Отформатировать сообщение."""
        return {"role": role, "text": message}

    async def __aupdate_context(self, key, value: dict[str, str]):
        """Асинхронно обновить контекст диалога в redis."""
        messages_s: str | None = await self.redis.get(name=key)
        if messages_s:
            messages: list = json.loads(messages_s)
        else:
            messages: list = []
        messages.append(value)
        await self.redis.set(
            name=key,
            value=json.dumps(messages),
            ex=self.redis_ttl,
        )
        logger.info("The context has been updated.")
        return messages

    def __update_context(self, key, value):
        """Синхронно обновить контекст в redis."""
        messages_s: str | None = self.redis.get(name=key)
        if messages_s:
            messages: list = json.loads(messages_s)
        else:
            messages: list = []
        messages.append(value)
        self.redis.set(name=key, value=json.dumps(messages), ex=self.redis_ttl)
        logger.info("The context has been updated.")
        return messages

    async def __aresponse_to_json(self, response: AsyncResponse):
        """Асинхронно преобразовать в словарь"""
        try:
            response_json = await response.json()
        except JSONDecodeError as e:
            logger.error(f"Response json parse error. Error: {e}.")
            return self.base_error_answer
        return response_json

    def __response_to_json(self, response: SyncResponse):
        """Синхронно преобразовать в словарь"""
        try:
            response_json = response.json()
        except JSONDecodeError as e:
            logger.error(f"Response json parse error. Error: {e}.")
            return self.base_error_answer
        return response_json

    def __parse_answer(self, response_json: dict):
        """Обработать ответ."""
        try:
            message_text = response_json["result"]["alternatives"][0][
                "message"
            ]["text"]
        except (KeyError, IndexError) as e:
            logger.error(
                "The response structure does not match the expected."
                f"Error: {e}"
            )
            return self.base_error_answer
        return message_text

    async def arequest(self, message: str, chat_uuid: str):
        """Асинхронный запрос к модели."""
        message = self.__format_message(message, role="user")
        messages = await self.__aupdate_context(key=chat_uuid, value=message)
        prompt = self.__set_prompt(messages)
        async with ClientSession(timeout=ClientTimeout(total=10)) as session:
            try:
                async with session.post(
                    url=self.YA_API_URL,
                    headers=self.__headers(),
                    json=prompt,
                ) as response:
                    if response.status != http.HTTPStatus.OK:
                        logger.error(
                            "The response from yandex gpt is not 200. "
                            "No response has been received."
                        )
                        return self.base_error_answer
                    response_json = await self.__aresponse_to_json(response)
                    response_text = self.__parse_answer(response_json)
                    response_format = self.__format_message(
                        response_text,
                        role="assistant",
                    )
                    _ = await self.__aupdate_context(
                        key=chat_uuid,
                        value=response_format,
                    )
            except asyncio.TimeoutError as e:
                logger.error(
                    "Yandex gpt did not respond in the allotted time."
                    f"Error: {e}"
                )
                return self.base_error_answer
            return response_text

    def request(self, message: str, chat_uuid: str):
        """Синхронный запрос к модели."""
        message = self.__format_message(message=message, role="user")
        messages = self.__update_context(key=chat_uuid, value=message)
        prompt = self.__set_prompt(messages)
        response = requests.post(
            url=self.YA_API_URL, headers=self.__headers(), json=prompt
        )
        if response.status_code != http.HTTPStatus.OK:
            logger.error(
                "The response from yandex gpt is not 200. "
                "No response has been received."
            )
            return self.base_error_answer
        logger.info(
            "The response from yandex gpt has been successfully received."
        )
        response_json = self.__response_to_json(response=response)
        response_text = self.__parse_answer(response_json=response_json)
        response_format = self.__format_message(
            message=response_text,
            role="assistant",
        )
        _ = self.__update_context(key=chat_uuid, value=response_format)
        return response_text
