# admin.py
from django.contrib import admin
from .models import User, Profile, Notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_ban', 'is_staff', 'is_admin', 'is_super_admin', 'is_verified')
    search_fields = ('email', 'username')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'date_of_birth')
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'content', 'is_read', 'created_at')  # Columns to display in the list view
    list_filter = ('is_read', 'created_at')  # Filters to display in the sidebar
    search_fields = ('user__email', 'title', 'content')  # Allow searching by user email, title, and content
    ordering = ('-created_at',)  # Order by creation date, descending
    readonly_fields = ('user', 'title', 'content', 'is_read', 'created_at')  # Make fields readonly in the detail view
