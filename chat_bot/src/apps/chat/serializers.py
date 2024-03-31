from rest_framework import serializers

from src.apps.chat.models import Chat, Dialog, Message


class DialogSerializer(serializers.ModelSerializer):
    """Сериализатор Диалогов."""

    first_message_text = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Dialog
        fields = (
            "id",
            "is_open",
            "first_message_text",
            "is_support_connected",
            "assessment",
            "created_date",
            "chat_id",
        )
        read_only_fields = ("__all__",)

    def get_first_message_text(self, obj: Dialog) -> str | None:
        first_message = Message.objects.filter(dialog_id=obj.id).first()
        return first_message.text if first_message else None


class ChatSerializer(serializers.ModelSerializer):
    """Сериализатор Чатов."""

    dialogs = DialogSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = (
            "id",
            "dialogs",
            "created_date",
            "user_id",
        )
        read_only_fields = ("__all__",)


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор Сообщений."""

    class Meta:
        model = Message
        fields = (
            "id",
            "text",
            "sender_type",
            "created_date",
            "chat_id",
            "dialog_id",
            "user_id",
        )
        read_only_fields = (
            "id",
            "sender_type",
            "created_date",
            "chat_id",
            "dialog_id",
            "user_id",
        )
