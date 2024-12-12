from django.shortcuts import render
from django.http import JsonResponse
import requests
from requests.exceptions import ConnectionError
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages  # Import messages module
from .models import Message
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def landing_page(request):
    return render(request, 'control/landing.html')

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Login the user
                login(request, user)
                return redirect('custom_admin')  # Redirect to the custom admin page (not default Django admin)
            else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = AuthenticationForm()

    return render(request, 'control/login.html', {'form': form})

def logout_view(request):
    logout(request)  # Logs the user out
    return redirect('login')  # Redirect to the login page (landing page) after logout

def custom_admin(request):
    messages_list = Message.objects.all()
    return render(request, 'control/custom_admin.html', {'messages': messages_list})

def users_list(request):
    users = User.objects.all()  # Fetch all users
    return render(request, 'control/users.html', {'users': users})

def update_status(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        message_id = data.get('id')
        try:
            message = Message.objects.get(id=message_id)
            message.is_read = True
            message.save()
            return JsonResponse({'success': True, 'message': 'Status updated'})
        except Message.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Message not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def delete_messages(request):
    if request.method == "POST":
        message_ids = request.POST.getlist('selected_messages')
        if message_ids:
            Message.objects.filter(id__in=message_ids).delete()
        return redirect('custom_admin')  # Updated to use the correct URL name
    return redirect('custom_admin')  # Also handle GET requests

@csrf_exempt
def delete_users(request):
    if request.method == "POST":
        user_ids = request.POST.getlist('selected_users')
        if user_ids:
            User.objects.filter(id__in=user_ids).delete()
        return redirect('users_list')
    return redirect('users_list')