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
      return None

    pwd_valid = check_password(password, drupal_user.pass_field)
    if drupal_user and pwd_valid:
      try:
        user = User.objects.get(username=username)
      except User.DoesNotExist:
        #TODO: Need add first_name and last_name fields
        user = User(
          username=username,
        )

        user.profile.avatar = str(drupal_user.picture) + '.png'
        user.profile.timezone = drupal_user.timezone
        user.profile.signature = drupal_user.signature

        user.set_password(password)
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

