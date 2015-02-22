from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """
    Allows a user to sign in using an email/password pair rather than
    """
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None


class FacebookAuthBackend(object):
    """
    Allows a user to sign in using an facebook account.
    """
    def authenticate(self, facebook_id=None):
        """
            Authenticate a user based on email address as the user name.
            Se asume que el fb_id es unico por usuario y no puede cambiar
        """
        try:
            return User.objects.get(fbprofile__fb_id=facebook_id)
        except User.DoesNotExist:
            return None
