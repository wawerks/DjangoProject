from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Message
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def store_message(request):
    try:
        data = json.loads(request.body)
        sender = data.get('sender')
        receiver = data.get('receiver')
        content = data.get('content')
        
        logger.info(f"Received message: sender={sender}, receiver={receiver}, content={content}")
        
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content
        )
        
        response_data = {
            'status': 'success',
            'message_id': message.id,
            'timestamp': message.timestamp.isoformat()
        }
        logger.info(f"Message stored successfully: {response_data}")
        return JsonResponse(response_data)
    except Exception as e:
        logger.error(f"Error storing message: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_http_methods(["GET"])
def get_messages(request):
    try:
        user = request.GET.get('user')
        if not user:
            return JsonResponse({
                'status': 'error',
                'message': 'User parameter is required'
            }, status=400)

        # Get both sent and received messages
        messages = Message.objects.filter(
            sender=user
        ).union(
            Message.objects.filter(receiver=user)
        ).order_by('-timestamp')

        return JsonResponse({
            'status': 'success',
            'messages': list(messages.values('id', 'sender', 'receiver', 'content', 'timestamp'))
        })
    except Exception as e:
        logger.error(f"Error retrieving messages: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to retrieve messages'
        }, status=500)
