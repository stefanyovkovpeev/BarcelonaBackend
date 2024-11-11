from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chatroom/messages/', consumers.ChatConsumer.as_asgi()),
]