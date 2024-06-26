from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("src.apps.api.urls"), name="api"),
    path("tg-bot/", include("src.apps.tg_bot.urls"), name="tg_bot"),
]
