from django.urls import path
from . import views  # Import the correct views module
from . import message_api

urlpatterns = [
    path('', views.landing_page, name='landing'),  # Reference landing_page, not index
    path('messages/store/', message_api.store_message, name='store_message'),
    path('messages/', message_api.get_messages, name='get_messages'),
]
