# medicapp_pro_backend/users/admin.py

from django.contrib import admin
from .models import User
from .access_models import AccessGrant


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'is_validated',
        'public_id'
    )
    list_filter = ('role', 'is_validated')


@admin.register(AccessGrant)
class AccessGrantAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'pharmacist',
        'is_confirmed',
        'is_active',
        'expires_at'
    )