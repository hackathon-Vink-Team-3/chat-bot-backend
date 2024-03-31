from django.urls import path
from src.apps.tg_bot import views

urlpatterns = [path("", views.web_hook_tg_bot)]
