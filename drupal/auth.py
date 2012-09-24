from django.contrib.auth.models import User

from models import DrupalUser
from functions import check_password

'''
This module need to authenticate users from Drupal database
and creating normal Django users if authenticated Drupal user is correct.
Just add 'drupal.auth.DrupalAuthenticate'
to tuple AUTHENTICATION_BACKENDS in settings.py.
'''

class DrupalAuthenticate(object):
  def authenticate(self, username=None, password=None):
    try:
      drupal_user = DrupalUser.objects.get(name=username)
    except DrupalUser.DoesNotExist:
      drupal_user = False

    pwd_valid = check_password(password, drupal_user.pass_field)
    if drupal_user and pwd_valid:
      try:
        user = User.objects.get(username=username)
      except User.DoesNotExist:
        # Create a new user. Note that we can set password
        # to anything, because it won't be checked; the password
        # from settings.py will.
        user = User(
          username=username,
          password=password,
        )

        user.profile.avatar = str(drupal_user.picture) + '.png'
        user.profile.timezone = drupal_user.timezone
        user.profile.signature = drupal_user.signature

        user.is_staff = False
        user.is_superuser = False
        user.save()
      return user
    return None

  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None

