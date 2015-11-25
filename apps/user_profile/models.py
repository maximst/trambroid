# -*- coding: utf-8 -*-
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from pytz import all_timezones
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import os

from trambroid import settings


class User(AbstractUser):
    avatar = ProcessedImageField(upload_to='avatars', blank=True,
                                default=os.path.join(settings.STATIC_URL,
                                                     'img/default_avatar.png'),
                                processors=[ResizeToFill(*settings.AVATAR_SIZE)],
                                format='JPEG',
                                options={'quality': 60})
    stupidity_level = models.SmallIntegerField(_(u'Уровень глупости'),
                    max_length=1, default=0, choices=settings.STUPIDITY_LEVELS)
    signature = models.CharField(_(u'Подпись'), max_length=255, blank=True,
                    default=('<img alt="" '
                        'src="http://www.trambroid.com/files/userbar.png" />'))
    timezone = models.CharField(_(u'Временная зона'), max_length=32,
            default='Europe/Kiev', choices=zip(all_timezones, all_timezones))
    language = models.CharField(_(u'Язык'), choices=settings.LANGUAGES,
                                                    max_length=5, default='ru')

    drupal_password = models.TextField(blank=True, null=True)
    drupal_uid = models.IntegerField(blank=True, null=True)
    drupal_blogs_alias_url = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        if self.get_full_name():
            return u'%s (%s)' % (self.get_full_name(), self.username)
        else:
            return u'%s' % self.username
