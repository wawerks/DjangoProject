from django.shortcuts import render
from django.http import JsonResponse
import requests
from requests.exceptions import ConnectionError
from django.conf import settings

# Create your views here.

def check_server_status():
    try:
        response = requests.get('http://localhost:8001/control/')
        return response.status_code == 200
    except ConnectionError:
        return False

def index(request):
    if not check_server_status():
        return JsonResponse({
            'status': 'error',
            'message': 'Server is not running'
        }, status=503)
    
    return JsonResponse({
        'status': 'ok',
        'message': 'Message API Server is running'
    })
