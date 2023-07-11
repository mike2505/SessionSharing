from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class DefaultCredentialsBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if username == 'admin' and password == 'admin':
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a user with the default credentials if it doesn't exist
                user = User.objects.create_user(username=username, password=password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            return user
        return None
