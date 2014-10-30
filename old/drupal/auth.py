from django.contrib.auth.models import User

from user_profile.models import UserProfile
from models import DrupalUser
from functions import check_password, split_name


class DrupalAuthenticate(object):
    '''
    This module need to authenticate users from Drupal database
    and creating normal Django users if authenticated Drupal user is correct.
    Just add 'drupal.auth.DrupalAuthenticate'
    to tuple AUTHENTICATION_BACKENDS in settings.py.
    '''

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
                user = User(
                    username=username,
                )

                user.first_name, user.last_name = split_name(drupal_user.name)
                user.email = drupal_user.mail
                user.set_password(password)
                user.is_staff = False
                user.is_superuser = False
                user.save()

                user_profile = UserProfile.objects.get(user=user)
                user_profile.avatar = str(drupal_user.picture) + '.png'
                user_profile.timezone = drupal_user.timezone
                user_profile.signature = drupal_user.signature
                user_profile.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
