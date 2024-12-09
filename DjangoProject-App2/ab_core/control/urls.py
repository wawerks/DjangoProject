from django.urls import path
from . import views  # Import the correct views module
from . import message_api
from . views import *

urlpatterns = [
    path('', views.login_page, name='landing'),  # Set the login page as the landing page
    path('custom-admin/', views.custom_admin, name='custom_admin'),

    path('messages/store/', message_api.store_message, name='store_message'),
    path('messages/', message_api.get_messages, name='get_messages'),
]
