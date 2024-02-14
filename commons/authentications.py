from django.contrib.auth.backends import ModelBackend, UserModel

from commons.deidentifications import pi_hasher


class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        username = pi_hasher.hashed_data(username)
        try:
            user = UserModel.objects.get(hashed_email=username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
