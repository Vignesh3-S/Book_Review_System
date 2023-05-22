from django.contrib.auth import get_user_model
from book.models import user
class EmailAuthBackend:
    def authenticate(self, email=None, password=None,usertype = None):
        try:
            userobj = user.objects.get(email=email,usertype = usertype)
            if userobj.check_password(password):
                return userobj
            return None
        except user.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            userobj = user.objects.get(pk=user_id)
            if userobj.is_active:
                return userobj
            return None
        except user.DoesNotExist:
            return None