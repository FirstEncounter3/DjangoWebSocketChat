# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.user_id = self.scope["user"].id
        self.user_name = self.scope["user"].username

        # Find room
        room = await database_sync_to_async(Room.objects.get)(room_name=self.room_name)

        # Create new chat
        chat = Message(
            message=message,
            user=self.scope['user'],
            room=room,
        )

        await database_sync_to_async(chat.save)()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": message,
                "user_id": self.user_id,
                "user_name": self.user_name,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user_id = event["user_id"]
        user_name = event["user_name"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "user_id": user_id,
            "user_name": user_name,
        }
        )
        )
