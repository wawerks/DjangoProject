from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

# Simulated message storage (You can replace this with a real database model later)
messages = []

# API endpoint to store a message
@csrf_exempt  # To handle POST requests without CSRF token
def store_message(request):
    if request.method == 'POST':
        try:
            # Parse incoming JSON body
            data = json.loads(request.body)
            sender = data.get('sender')
            receiver = data.get('receiver')
            content = data.get('content')

            # Basic validation (You can add more checks here)
            if not sender or not receiver or not content:
                return JsonResponse({'status': 'error', 'message': 'Missing sender, receiver, or content.'})

            # Add the message to the simulated storage (list)
            message = {
                "sender": sender,
                "receiver": receiver,
                "content": content,
                "timestamp": timezone.now().isoformat()  # Use current timestamp
            }
            messages.append(message)

            # Return a successful response
            return JsonResponse({'status': 'success', 'message': 'Message sent successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid method. Use POST.'})

# API endpoint to retrieve messages
def get_messages(request):
    user = request.GET.get('user')
    if user:
        # Filter messages by the user (sender or receiver)
        user_messages = [msg for msg in messages if msg['sender'] == user or msg['receiver'] == user]
        
        if user_messages:
            return JsonResponse({'status': 'success', 'messages': user_messages})
        else:
            return JsonResponse({'status': 'error', 'message': 'No messages found for this user.'})
    return JsonResponse({'status': 'error', 'message': 'User not specified.'})
