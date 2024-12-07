from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
import json
from .models import ChatGroup
from django.template.loader import render_to_string
from .services import MessageService
from django.utils import timezone
import logging
from django.conf import settings
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)
f = Fernet(settings.ENCRYPT_KEY)

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
        try:
            text_data_json = json.loads(text_data)
            body = text_data_json['body']
            logger.info(f"Received message from WebSocket: user={self.user.username}")

            # Encrypt message before storing
            message_bytes = body.encode('utf-8')
            encrypted_message = f.encrypt(message_bytes)
            encrypted_message_str = encrypted_message.decode('utf-8')

            # Store encrypted message in App2's database
            message_data = self.message_service.store_message(
                sender=self.user.username,
                receiver=self.chatroom_name,
                content=encrypted_message_str
            )

            if not message_data or message_data.get('status') != 'success':
                logger.error(f"Failed to store message: {message_data}")
                self.send(text_data=json.dumps({
                    'error': 'Failed to store message'
                }))
                return

            logger.info("Message stored successfully")

            # Create message object for template (using original message)
            message = {
                'body': body,  # Use unencrypted message for display
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
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            self.send(text_data=json.dumps({
                'error': 'Invalid message format'
            }))
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            self.send(text_data=json.dumps({
                'error': 'Failed to process message'
            }))

    def message_handler(self, event):
        message = event['message']
        logger.info(f"Handling message event: {event}")
        
        self.send(text_data=message)

    def chat_message(self, event):
        try:
            message_data = json.loads(event['message'])
            
            # If the current user is the sender, use the sender HTML
            if self.user.username == message_data['author']:
                message_data['html'] = message_data['html_sender']
            
            # Send message to WebSocket
            self.send(text_data=json.dumps(message_data))
        except Exception as e:
            logger.error(f"Error sending chat message: {str(e)}")
            self.send(text_data=json.dumps({
                'error': 'Failed to send message'
            }))
