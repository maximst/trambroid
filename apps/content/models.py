from django.db import models
from django.conf import settings
from django.urls import reverse

from parler.models import TranslatableModel, TranslatedFields
from taggit.managers import TaggableManager
from taggit.models import TaggedItem
import mptt
import re


class Blog(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=128),
        preview = models.TextField(default='', blank=True),
        body = models.TextField(default=''),
    )
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING)
    front_page = models.BooleanField(default=True)
    on_top = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True,
                                       editable=True)
    edit_time = models.DateTimeField(auto_now=True, auto_now_add=False,
                                     editable=True)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    drupal_nid = models.IntegerField(default=0, max_length=10, blank=True)
    drupal_slug = models.CharField(max_length=255, default='', blank=True)
    drupal_type = models.CharField(max_length=10, default='blog', blank=True)
    tags = TaggableManager(through=TaggedItem)
    in_menu = models.BooleanField(default=False)

    def __unicode__(self):
        return self.safe_translation_getter('title', 'Blog: %s' % self.pk)

    def get_absolute_url(self):
        return reverse('content:detail', args=[str(self.slug)])

    def get_tags(self, **kwargs):
        return self.tags.filter(**kwargs)

    def get_comments(self):
        return Comment.objects.filter(blog_id=self.id).order_by('-create_time')


@mptt.register
class Comment(models.Model):
    title = models.CharField(max_length=64, blank=True, default='')
    body = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True,
                                       editable=True)
    edit_time = models.DateTimeField(auto_now=True, auto_now_add=False,
                                     editable=True)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child', on_delete=models.DO_NOTHING)
    language = models.CharField(max_length=5, default='ru', choices=settings.LANGUAGES)

    def __unicode__(self):
        return u'%s: %s - %s' % (self.user, self.blog, self.body[:32])

    def body_only(self):
        r = re.compile(settings.QUOTE_REGEX, re.I+re.S)
        new_body = r.sub('', self.body)

        return new_body

    def full_body(self):
        if not self.title or self.title in self.body:
            return self.body
        else:
            return u'{} {}'.format(self.title, self.body)
