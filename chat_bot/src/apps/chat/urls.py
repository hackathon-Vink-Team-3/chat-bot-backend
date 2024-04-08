from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.apps.chat.views import ChatViewSet, DialogViewSet

router = DefaultRouter()
router.register(r"chat", ChatViewSet, "chat")
router.register(
    r"chat/(?P<chat_uuid>[0-9a-f\-]+)/dialog", DialogViewSet, "dialog"
)

urlpatterns = [
    path("", include(router.urls)),
]
