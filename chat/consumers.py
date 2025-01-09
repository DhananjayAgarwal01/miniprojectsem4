import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.user = self.scope["user"]
        self.other_user_id = int(self.scope['url_route']['kwargs']['user_id'])
        
        try:
            self.other_user = await self.get_user(self.other_user_id)
            if not self.other_user:
                await self.close()
                return
        except User.DoesNotExist:
            await self.close()
            return

        # Create unique room name for the chat
        self.room_name = f"chat_{min(self.user.id, self.other_user_id)}_{max(self.user.id, self.other_user_id)}"
        self.room_group_name = f"chat_{self.room_name}"
        
        # Create a presence channel for each user
        self.user_presence_group = f"presence_{self.user.id}"
        self.other_user_presence_group = f"presence_{self.other_user_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Join presence groups
        await self.channel_layer.group_add(
            self.user_presence_group,
            self.channel_name
        )
        await self.channel_layer.group_add(
            self.other_user_presence_group,
            self.channel_name
        )

        await self.accept()
        
        # Broadcast user's online status
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'user_id': self.user.id,
                'status': 'online'
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'room_group_name'):
            # Broadcast user's offline status
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'user_id': self.user.id,
                    'status': 'offline'
                }
            )
            
            # Leave all groups
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            if hasattr(self, 'user_presence_group'):
                await self.channel_layer.group_discard(
                    self.user_presence_group,
                    self.channel_name
                )
            if hasattr(self, 'other_user_presence_group'):
                await self.channel_layer.group_discard(
                    self.other_user_presence_group,
                    self.channel_name
                )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            
            if 'type' in text_data_json:
                if text_data_json['type'] == 'typing':
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'typing_status',
                            'sender_id': self.user.id
                        }
                    )
                    return
                elif text_data_json['type'] == 'stop_typing':
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'stop_typing_status',
                            'sender_id': self.user.id
                        }
                    )
                    return
            
            message = text_data_json.get('message', '').strip()
            if not message:
                return
            
            # Save message to database
            await self.save_message(message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': self.user.id,
                    'sender_username': self.user.username
                }
            )
        except json.JSONDecodeError:
            pass
        except KeyError:
            pass

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username']
        }))

    async def typing_status(self, event):
        # Send typing status to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender_id': event['sender_id']
        }))

    async def stop_typing_status(self, event):
        # Send stop typing status to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'stop_typing',
            'sender_id': event['sender_id']
        }))

    async def user_status(self, event):
        # Send user status to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'status',
            'user_id': event['user_id'],
            'status': event['status']
        }))

    @database_sync_to_async
    def save_message(self, message):
        Message.objects.create(
            sender=self.user,
            recipient=self.other_user,
            content=message
        )

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None 