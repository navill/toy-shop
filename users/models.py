import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager as _UserManager
from django.db import models
from safedelete.managers import SafeDeleteManager

from commons.deidentifications import pi_masker, pi_cipher
from commons.models import CommonModel
from users.mixins import DeidentificationMixin


class UserManager(SafeDeleteManager, _UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        password = make_password(password)
        user = self.model(username=username, email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user


class User(DeidentificationMixin, CommonModel, AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    ci = models.BinaryField(unique=True)
    email = models.BinaryField(unique=True)
    hashed_email = models.BinaryField(unique=True)
    username = models.BinaryField()

    nickname = models.CharField(max_length=20, unique=True)
    phone = models.BinaryField()

    address = models.CharField(max_length=256, null=True, blank=True)
    detail_address = models.BinaryField(null=True, blank=True)
    shipping_address = models.CharField(max_length=256, null=True, blank=True)
    detail_shipping_address = models.BinaryField(null=True, blank=True)

    groups = None
    user_permissions = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = UserManager()

    def __str__(self):
        return self.masked_email
