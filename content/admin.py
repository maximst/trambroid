from django.contrib import admin
from hvad.admin import TranslatableAdmin
from models import Blog

class BlogAdmin(TranslatableAdmin):
    list_display = ('__unicode__', 'author', 'create_time', 'all_translations',
                                            'front_page', 'on_top', 'deleted')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Blog, BlogAdmin)
