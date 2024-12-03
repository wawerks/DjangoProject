from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
import json
from .models import ChatGroup
from django.template.loader import render_to_string
from .services import MessageService
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        self.message_service = MessageService()
        
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )
        self.accept()
        logger.info(f"WebSocket connected: user={self.user.username}, chatroom={self.chatroom_name}")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )
        logger.info(f"WebSocket disconnected: user={self.user.username}, chatroom={self.chatroom_name}")

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        logger.info(f"Received message from WebSocket: user={self.user.username}, body={body}")

        # Store message in App2's database
        message_data = self.message_service.store_message(
            sender=self.user.username,
            receiver=self.chatroom_name,
            content=body
        )
        logger.info(f"Store message response: {message_data}")

        # Create message object for template
        message = {
            'body': body,
            'author': self.user.username,
            'timestamp': timezone.now()
        }

        # Render message HTML for initial sender
        html_sender = render_to_string('a_rtchat/message.html', {
            'message': message,
            'user': {'username': self.user.username}
        })

        # Render message HTML for receivers
        html_receiver = render_to_string('a_rtchat/message.html', {
            'message': message,
            'user': {'username': ''}  # Empty username so it renders as received message
        })

        # Broadcast message to group
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,
            {
                'type': 'chat_message',
                'message': json.dumps({
                    'html': html_receiver,
                    'html_sender': html_sender,
                    'author': self.user.username
                })
            }
        )

    def message_handler(self, event):
        message = event['message']
        logger.info(f"Handling message event: {event}")
        
        self.send(text_data=message)

    def chat_message(self, event):
        message_data = json.loads(event['message'])
        
        # If the current user is the sender, use the sender HTML
        if self.user.username == message_data['author']:
            message_data['html'] = message_data['html_sender']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps(message_data))
