from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ChatmessageCreateForm
from .services import MessageService
from django.utils.dateparse import parse_datetime
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

from django.conf import settings
from cryptography.fernet import Fernet


f = Fernet(settings.ENCRYPT_KEY)


@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")
    message_service = MessageService()
    
    # Get messages from App2's database
    response = message_service.get_messages(chat_group.group_name)
    chat_messages = []
    if response and response.get('status') == 'success':
        messages_data = response.get('messages', [])
        for msg in messages_data:
            try:
                # Decrypt the message content
                encrypted_content = msg['content'].encode('utf-8')
                decrypted_bytes = f.decrypt(encrypted_content)
                decrypted_content = decrypted_bytes.decode('utf-8')
                
                print('encrypted_content:',encrypted_content)
                print('decrypted_bytes:',decrypted_bytes)
                print('decrypted_content:',decrypted_content)

                chat_messages.append({
                    'body': decrypted_content,
                    'author': msg['sender'],
                    'timestamp': parse_datetime(msg['timestamp'])
                })
            except Exception as e:
                logger.error(f"Error decrypting message: {str(e)}")
                # Skip messages that can't be decrypted
                continue
    
    form = ChatmessageCreateForm()

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            try:
                body = form.cleaned_data['body']
                
                # Encrypt message
                message_bytes = body.encode('utf-8')
                encrypted_message = f.encrypt(message_bytes)
                encrypted_message_str = encrypted_message.decode('utf-8')
                
                print('message_bytes:',message_bytes)
                print('encrypted_message:',encrypted_message)
                print('encrypted_message_str:',encrypted_message_str)
                
                # Store the encrypted message
                response = message_service.store_message(
                    sender=request.user.username,
                    receiver=chat_group.group_name,
                    content=encrypted_message_str
                )
                
                if not response or response.get('status') != 'success':
                    logger.error(f"Failed to store message: {response}")
                    raise Exception("Failed to store message")

                context = {
                    'message': {
                        'body': body,
                        'author': request.user.username,
                        'timestamp': timezone.now()
                    },
                    'user': request.user
                }
                return render(request, 'a_rtchat/message.html', context)
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Failed to process message'
                }, status=500)
    
    return render(request, 'a_rtchat/chat.html', {
        'chat_messages': chat_messages,
        'form': form,
        'user': request.user
    })

def home_view(request):
    return HttpResponse("<h1>Welcome to Chat</h1><a href='/chat/'>Join Chat</a>")

def index_view(request):
    # Create default public chat if it doesn't exist
    ChatGroup.objects.get_or_create(
        group_name="public-chat",
        defaults={
            'description': 'Public Chat Room'
        }
    )
    
    chat_groups = ChatGroup.objects.all()
    return render(request, 'a_rtchat/index.html', {'chat_groups': chat_groups})
