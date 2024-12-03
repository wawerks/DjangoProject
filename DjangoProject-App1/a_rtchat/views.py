from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ChatmessageCreateForm
from .services import MessageService
from django.utils.dateparse import parse_datetime
from django.utils import timezone


@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")
    message_service = MessageService()
    
    # Get messages from App2's database
    response = message_service.get_messages(chat_group.group_name)
    chat_messages = []
    if response and response.get('status') == 'success':
        messages_data = response.get('messages', [])
        chat_messages = [{
            'body': msg['content'],
            'author': msg['sender'],
            'timestamp': parse_datetime(msg['timestamp'])
        } for msg in messages_data]
    
    form = ChatmessageCreateForm()

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            # We don't need to save to local DB anymore since messages are stored in App2
            context = {
                'message': {
                    'body': body,
                    'author': request.user.username,
                    'timestamp': timezone.now()
                },
                'user': request.user
            }
            return render(request, 'a_rtchat/message.html', context)

    return render(request, 'a_rtchat/chat.html', {
        'chat_messages': chat_messages,
        'form': form,
        'user': request.user
    })
