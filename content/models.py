from django.db import models
from django.contrib.auth.models import User

from hvad.models import TranslatableModel, TranslatedFields

from tag.models import ArticleTaggedItem, TaggableManagerN


class Blog(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=128),
        preview = models.TextField(default='', blank=True),
        body = models.TextField(default=''),
    )
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    deleted = models.BooleanField(default=False)
    author = models.ForeignKey(User, null=True)
    front_page = models.BooleanField(default=True)
    on_top = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    nid = models.IntegerField(default=0, max_length=10, blank=True)
    drupal_slug = models.CharField(max_length=255, default='', blank=True)
    tags = TaggableManagerN(through=ArticleTaggedItem)

    def __unicode__(self):
        return self.safe_translation_getter('title', 'Blog: %s' % self.pk)