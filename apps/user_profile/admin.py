from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


@admin.register(get_user_model())
class UserAdmin(DjangoUserAdmin):
    list_display = (
        'username',
        'email',
        'get_full_name',
        'language',
        'drupal_uid',
        'is_active',
        'is_superuser', 
        'is_staff')

    fieldsets = DjangoUserAdmin.fieldsets
    fieldsets[1][1]['fields'] += (
        'language',
        'timezone',
        'avatar',
        'stupidity_level',
        'signature',
    )