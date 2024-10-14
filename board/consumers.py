import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage, Drawing, Room


class WhiteBoardAndChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'whiteboardandchat_{self.room_name}'

        self.user = self.scope['user']
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'draw':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'draw_shape',
                    'shape': data['shape'],
                    'color': data['color'],
                    'x': data.get('x'),
                    'y': data.get('y'),
                    'width': data.get('width'),
                    'height': data.get('height'),
                    'radius': data.get('radius'),
                    'points': data.get('points'),
                }
            )
        elif data['type'] == 'chat_message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data['message'],
                    'user': data['user'],
                }
            )
        elif data['type'] == 'clear':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'clear_board',
                }
            )

    async def draw_shape(self, event):
        await self.send(text_data=json.dumps({
            'type': 'draw',
            'shape': event['shape'],
            'color': event['color'],
            'x': event.get('x'),
            'y': event.get('y'),
            'width': event.get('width'),
            'height': event.get('height'),
            'radius': event.get('radius'),
            'points': event.get('points'),
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'user': event['user'],
        }))

    async def clear_board(self, event):
        await self.send(text_data=json.dumps({
            'type': 'clear',
        }))
    

@database_sync_to_async
def save_message(self, message):
    room = Room.objects.get(name=self.room_name)
    ChatMessage.objects.create(room=room, message=message, user=self.scope['user'])