from rest_framework import serializers

from users.exceptions import UserExceptions
from users.models import User
from users.services import user_service


class UserCreateRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    username = serializers.CharField()
    nickname = serializers.CharField()
    phone = serializers.CharField()

    address = serializers.CharField(required=False)
    detail_address = serializers.CharField(required=False)
    shipping_address = serializers.CharField(required=False)
    detail_shipping_address = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "username",
            "nickname",
            "phone",
            "address",
            "detail_address",
            "shipping_address",
            "detail_shipping_address",
        ]

    def create(self, validated_data):
        try:
            dto = user_service.get_user_dto(**validated_data)
            return user_service.join(dto)
        except Exception as e:
            raise UserExceptions.UserException(detail=e)


class UserUpdateRequestSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    shipping_address = serializers.CharField(required=False)
    detail_address = serializers.CharField(required=False)
    detail_shipping_address = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "nickname",
            "address",
            "detail_address",
            "shipping_address",
            "detail_shipping_address"
        ]

    def validate(self, attrs):
        if not attrs:
            raise UserExceptions.UserException(detail="최소 한 가지 필드는 입력해주세요")
        return attrs

    def update(self, instance, validated_data):
        try:
            dto = user_service.get_user_dto(**validated_data)
            return user_service.update(instance, dto)
        except Exception as e:
            raise UserExceptions.UserException(detail=e)
