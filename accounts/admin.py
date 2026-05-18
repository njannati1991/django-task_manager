from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserAvatar


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {
            'fields': ('national_id', 'mobile', 'birthday')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {
            'fields': ('national_id', 'email', 'mobile', 'birthday')
        }),
    )