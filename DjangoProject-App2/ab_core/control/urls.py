from django.urls import path
from . import views  # Import the correct views module
from . import message_api
from . views import *

urlpatterns = [
    path('', views.login_page, name='login'),  # Rename this to 'login'
    path('custom-admin/', views.custom_admin, name='custom_admin'),
    path('update-status/', views.update_status, name='update_status'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.users_list, name='users_list'),

    path('messages/store/', message_api.store_message, name='store_message'),
    path('messages/', message_api.get_messages, name='get_messages'),
]
