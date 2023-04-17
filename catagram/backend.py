from django.contrib.auth.backends import BaseBackend
from .models import UserProfile

class MyCustomUserBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        else:
            return None