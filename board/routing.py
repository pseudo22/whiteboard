from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/whiteboardandchat/<str:room_name>/', consumers.WhiteBoardAndChatConsumer.as_asgi()),
]
