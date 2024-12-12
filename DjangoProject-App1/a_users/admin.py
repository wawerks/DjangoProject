from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.html import format_html
from .models import Profile

# Unregister the default User admin
admin.site.unregister(User)

# Define a new User admin
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

# Registering Profile model in Django admin with avatar display
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'displayname', 'show_avatar')
    search_fields = ('user__username', 'displayname')
    list_filter = ('user__is_active',)

    def show_avatar(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.image.url)
        return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar)
    show_avatar.short_description = 'Avatar'
