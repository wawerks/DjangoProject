from django.urls import path
from . import message_api

urlpatterns = [
    path('messages/store/', message_api.store_message, name='store_message'),
    path('messages/', message_api.get_messages, name='get_messages'),
]
