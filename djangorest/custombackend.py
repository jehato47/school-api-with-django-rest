from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class MyBackend(object):
    def authenticate(self, request, username=None, password=None):

        if request is not None:
            db = request.path.split("/")[1]
            u = User.objects.using(db).filter(username=username).first()
        else:
            u = User.objects.get(username=username)
        if u and u.check_password(password):
            return u
        else:
            return None

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None



