from rest_framework import serializers

from commons.deidentifications import pi_cipher


class DecryptedSerializerField(serializers.CharField):
    def to_representation(self, value):
        return pi_cipher.decrypt(value)
