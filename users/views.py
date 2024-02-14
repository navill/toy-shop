from distutils.util import strtobool

from rest_framework.permissions import AllowAny

from commons.permissions import IsOwner
from commons.views import generics
from users.models import User
from users.serializers.request_serializers import UserCreateRequestSerializer, UserUpdateRequestSerializer
from users.serializers.response_serializers import UserMaskedResponseSerializer, UserDecryptedResponseSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    request_serializer_class = UserCreateRequestSerializer
    response_serializer_class = UserMaskedResponseSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsOwner]
    response_serializer_class = UserMaskedResponseSerializer
    lookup_field = "uuid"


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsOwner]
    request_serializer_class = UserUpdateRequestSerializer
    response_serializer_class = UserDecryptedResponseSerializer
    lookup_field = "uuid"
