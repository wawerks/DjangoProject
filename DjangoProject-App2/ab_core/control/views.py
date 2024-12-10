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


def custom_admin(request):
    messages_list = Message.objects.all()
    return render(request, 'control/custom_admin.html', {'messages': messages_list})