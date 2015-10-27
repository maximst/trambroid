from django.contrib.auth import get_user_model

from functions import check_password


User = get_user_model()


class DrupalAuthenticate(object):
    '''
    This module need to authenticate users from Drupal database
    and creating normal Django users if authenticated Drupal user is correct.
    Just add 'drupal.auth.DrupalAuthenticate'
    to tuple AUTHENTICATION_BACKENDS in settings.py.
    '''

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        pwd_valid = check_password(password, user.drupal_password)
        if pwd_valid:
            print user.password
            if not user.password:
                user.set_password(password)
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
