# ab_core/control/urls.py
from django.urls import path
from . import views

# URL patterns for the 'control' app
urlpatterns = [
    path('', views.index, name='index'),  # Maps to the index view
    path('store/', views.store_message, name='store_message'),  # Store message endpoint
    path('get/', views.get_messages, name='get_messages'),  # Get messages endpoint
]
