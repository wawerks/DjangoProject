from django.shortcuts import render
from ab_core.control.message_api import store_message as store_message_func, get_messages as get_messages_func  # Renamed the functions

def index(request):
    return render(request, 'control/home.html')  # Render home.html from control app templates

def store_message(request):
    if request.method == 'POST':
        return store_message_func(request)  # Calls the renamed store_message function

def get_messages(request):
    if request.method == 'GET':
        return get_messages_func(request)  # Calls the renamed get_messages function
