from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .api_views import UserViewSet, ChatGroupViewSet, MessageViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', ChatGroupViewSet)

urlpatterns = [
    # Original views
    path('', index_view, name="home"),
    path('chat/', chat_view, name="chat"),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/groups/<int:group_pk>/messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='group-messages'),
]
