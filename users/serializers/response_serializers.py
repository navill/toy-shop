from rest_framework import serializers

from users.models import User


class UserMaskedResponseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="masked_username")
    phone = serializers.CharField(source="masked_phone")
    detail_address = serializers.CharField(source="masked_detail_address")
    detail_shipping_address = serializers.CharField(source="masked_detail_shipping_address")

    class Meta:
        model = User
        fields = [
            "uuid",
            "username",
            "phone",
            "nickname",
            "address",
            "detail_address",
            "shipping_address",
            "detail_shipping_address"
        ]


class UserDecryptedResponseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="decrypted_username")
    phone = serializers.CharField(source="decrypted_phone")
    detail_address = serializers.CharField(source="decrypted_detail_address")
    detail_shipping_address = serializers.CharField(source="decrypted_detail_shipping_address")

    class Meta:
        model = User
        fields = [
            "uuid",
            "username",
            "phone",
            "nickname",
            "address",
            "detail_address",
            "shipping_address",
            "detail_shipping_address"
        ]
