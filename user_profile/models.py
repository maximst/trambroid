from django.db import models
from django.contrib.auth.models import User

from pytz import all_timezones

from trambroid import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    avatar = models.ImageField(upload_to='user_avatars', blank=True,
                                default='user_avatars/default.png')
    stupidity_level = models.SmallIntegerField(max_length=1, default=0,
                                            choices=settings.STUPIDITY_LEVELS)
    signature = models.CharField(max_length=255, blank=True,
                                      default=('<img alt="" '
                                      'src="http://www.trambroid.com'
                                      '/files/userbar.png" />'))
    timezone = models.CharField(max_length=32, default='Europe/Kiev',
                                  choices=zip(all_timezones, all_timezones))

    def __unicode__(self):
        if self.user.get_full_name():
            return u'%s' % (self.user.get_full_name())
        else:
            return u'%s' % self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
