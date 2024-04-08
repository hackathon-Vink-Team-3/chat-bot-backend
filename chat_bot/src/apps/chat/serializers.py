from rest_framework import serializers

from src.apps.chat.models import Chat, Dialog, Message


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


class DialogDetailSerializer(serializers.ModelSerializer):
    """Сериализатор Диалога."""

    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Dialog
        fields = (
            "id",
            "is_open",
            "messages",
            "is_support_connected",
            "assessment",
            "created_date",
            "chat_id",
        )
        read_only_fields = (
            "id",
            "is_support_connected",
            "created_date",
            "chat_id",
        )


class DialogListSerializer(serializers.ModelSerializer):
    """Сериализатор списка Диалогов."""

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
        read_only_fields = (
            "id",
            "first_message_text",
            "is_support_connected",
            "created_date",
            "chat_id",
        )

    def get_first_message_text(self, obj: Dialog) -> str | None:
        first_message = Message.objects.filter(dialog_id=obj.id).last()
        return first_message.text if first_message else None

    def create(self, validated_data):
        chat_uuid = validated_data["chat_id"]
        open_dialog = Dialog.objects.filter(
            chat_id=chat_uuid,
            is_open=True,
        ).first()
        if open_dialog:
            open_dialog.is_open = False
            open_dialog.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        is_open = validated_data.get("is_open")
        if is_open:
            open_dialog = Dialog.objects.filter(
                is_open=True, chat_id=instance.chat_id
            ).first()
            if open_dialog:
                raise serializers.ValidationError(
                    detail={"error": "Открытый диалог уже существует."}
                )
        return super().update(instance, validated_data)


class ChatSerializer(serializers.ModelSerializer):
    """Сериализатор Чата."""

    dialogs = DialogListSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = (
            "id",
            "dialogs",
            "created_date",
            "user_id",
        )
        read_only_fields = ("__all__",)
