from django.contrib import admin
from models import DrupalUser

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'uid', 'mail', 'signature')

admin.site.register(DrupalUser, UserAdmin)