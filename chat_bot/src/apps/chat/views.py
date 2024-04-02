from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.apps.chat.models import Chat, Dialog
from src.apps.chat.serializers import (
    ChatSerializer,
    DialogListSerializer,
    DialogDetailSerializer,
)
from src.apps.users.models import CustomUser


class ChatViewSet(mixins.CreateModelMixin, GenericViewSet):
    """Чаты."""

    serializer_class = ChatSerializer
    swagger_tags = ["CHAT"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Chat.objects.none()
        return Chat.objects.all()

    def create(self, request, *args, **kwargs) -> Response:
        """
        Создать Чат.
        -- Если пользователь авторизован, объект чата который ссылается на
            пользователя выполняющего запрос.
        -- Если пользователь не авторизован, вернется объект чата найденный по
            ключу сессии.
        -- Если нет ключа сессии или чат по ключу не найден, создается и
            возвращается новый объект чата.
        """
        user: CustomUser = request.user
        if user.is_authenticated:
            # При создании пользователя должен создаваться чат.
            chat = Chat.objects.filter(user_id=user.id).first()
            return Response(
                self.serializer_class(instance=chat).data,
                status=status.HTTP_200_OK,
            )
        chat_uuid = request.session.get("chat_uuid")
        chat = Chat.objects.filter(id=chat_uuid).first()
        if chat:
            return Response(
                self.serializer_class(instance=chat).data,
                status=status.HTTP_200_OK,
            )
        else:
            serializer = self.serializer_class(
                data={"user": user if user.is_authenticated else None}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            request.session["chat_uuid"] = serializer.data["id"]
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )


class DialogViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    """Диалоги."""

    http_method_names = ["get", "post", "patch"]
    swagger_tags = ["DIALOG"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Dialog.objects.none()
        return Dialog.objects.filter(chat_id=self.kwargs.get("chat_uuid"))

    def get_serializer_class(self):
        if self.action == "list":
            return DialogListSerializer
        else:
            return DialogDetailSerializer

    def create(self, request, *args, **kwargs):
        """
        Создать диалог.
        Диалог создается только если нет открытого диалога,
        иначе возвращается открытый диалог.
        """
        chat_uuid = kwargs["chat_uuid"]
        open_dialog = (
            self.get_queryset().filter(chat_id=chat_uuid, is_open=True).first()
        )
        serializer = self.get_serializer_class()
        if open_dialog:
            return Response(
                serializer(instance=open_dialog).data,
                status=status.HTTP_200_OK,
            )
        serializer = serializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save(chat_id=chat_uuid)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Получить диалог.
        """
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        Получить список диалогов.
        """
        return super().list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Изменение диалога.
        Нельзя изменить значение is_open на true если есть другой диалог
        в этом чате со значением is_open=true
        """
        return super().partial_update(request, *args, **kwargs)
