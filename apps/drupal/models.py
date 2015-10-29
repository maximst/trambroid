from django.db import models
from django.conf import settings

from apps.content.models import Blog

import mptt


@mptt.register
class Forum(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    weight = models.IntegerField(default=0, blank=True)
    language = models.CharField(max_length=5, default='ru', choices=settings.LANGUAGES)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child')
    blogs = models.ManyToManyField('content.Blog')
    tid = models.IntegerField(default=0, blank=True)
    url = models.CharField(max_length=255, null=True, default=None)

    def get_blogs(self):
        blogs = self.blogs.all().annotate(comment_count=models.Count('comment',
                    distinct=True), tags_count=models.Count('tags',
                    distinct=True)).order_by('-create_time')
        return blogs
