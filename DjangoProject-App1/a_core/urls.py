"""
URL configuration for a_core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from a_users.views import profile_view
from a_home.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    # Admin and authentication
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # API endpoints
    path('api/', include(router.urls)),  # Auto-generated API endpoints
    path('api/auth/', include('rest_framework.urls')),  # DRF browsable API auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/chat/', include('a_rtchat.urls')),  # Chat API endpoints
    
    # Original app URLs
    path('', include('a_rtchat.urls')),
    path('profile/', include('a_users.urls')),
    path('@<username>/', profile_view, name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
