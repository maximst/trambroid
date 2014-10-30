from django.contrib import admin
from hvad.admin import TranslatableAdmin
from models import Blog, Comment

class BlogAdmin(TranslatableAdmin):
    list_display = ('__unicode__', 'user', 'create_time', 'all_translations',
                                            'front_page', 'on_top', 'deleted')
    prepopulated_fields = {'slug': ('name',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'create_time', 'ip')


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)

