from django.contrib import admin
from .models import *

# Unregister models to remove them from admin interface
if admin.site.is_registered(ChatGroup):
    admin.site.unregister(ChatGroup)
if admin.site.is_registered(GroupMessage):
    admin.site.unregister(GroupMessage)