from django.shortcuts import render
from django.http import JsonResponse
import requests
from requests.exceptions import ConnectionError
from django.conf import settings

# Create your views here.

from django.shortcuts import render

def landing_page(request):
    return render(request, 'control/landing.html')
