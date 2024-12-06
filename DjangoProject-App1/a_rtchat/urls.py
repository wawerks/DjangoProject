from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name="home"),
    path('chat/', chat_view, name="chat"),
]
