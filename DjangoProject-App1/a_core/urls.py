"""
URL configuration for a_core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from a_users.views import profile_view

urlpatterns = [
    # Admin and authentication
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # Original app URLs
    path('', include('a_rtchat.urls')),
    path('profile/', include('a_users.urls')),
    path('@<username>/', profile_view, name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
