from django.db import transaction
from rest_framework import serializers

from items.exceptions import CategoryExceptions
from items.models import Category, Product, CategoryPosition


class CategoryPositionUpdateSerializer(serializers.ModelSerializer):
    target_id = serializers.IntegerField(write_only=True)
    position = serializers.ChoiceField(choices=CategoryPosition, write_only=True)

    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    type_name = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ["target_id", "parent", "position", "type_name"]

    def validate(self, attrs):
        target_id = attrs.get("target_id")

        if not Category.objects.filter(id=target_id).exists():
            raise CategoryExceptions.NotFoundCategory()

        return attrs

    def update(self, instance, validated_data):
        target = Category.objects.get(id=validated_data["target_id"])

        with transaction.atomic():
            instance.move_to(target=target, position=validated_data["position"])
            instance.save()
        return instance


class CategoryNameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["type_name"]


class ProductUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field="uuid", required=False)
    name = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    stock = serializers.IntegerField(required=False, min_value=1, max_value=9_999)
    initial_stock = serializers.IntegerField(required=False, min_value=1, max_value=9_999)
    price = serializers.IntegerField(required=False, min_value=1000, max_value=10_000_000)

    class Meta:
        model = Product
        fields = ["category", "name", "content", "stock", "initial_stock", "price", "selling"]
