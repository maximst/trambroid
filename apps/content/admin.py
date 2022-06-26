from django.contrib import admin
from django.contrib.admin.widgets import AdminTextareaWidget, AdminTextInputWidget
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm, TranslatedField
from .models import Blog, Comment

class BlogAdminForm(TranslatableModelForm):
    title = TranslatedField(widget=AdminTextInputWidget)
    preview = TranslatedField(widget=AdminTextareaWidget)
    body = TranslatedField(widget=AdminTextareaWidget)


class BlogAdmin(TranslatableAdmin):
    list_display = ('__unicode__', 'user', 'create_time', 'all_languages_column',
                                            'front_page', 'on_top', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug', 'drupal_nid', 'drupal_slug')
    list_filter = ('is_active', 'front_page', 'on_top', 'drupal_type')

    form = BlogAdminForm


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'create_time', 'ip')


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)

