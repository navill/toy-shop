from django.db import transaction
from rest_framework import serializers

from items.exceptions import CategoryExceptions
from items.models import Category, Product, CategoryPosition

POSITION_LIST = ["first-child", "last-child", "left", "right"]


class CategoryCreateRequestSerializer(serializers.ModelSerializer):
    target_id = serializers.IntegerField(required=False)
    parent = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    position = serializers.ChoiceField(choices=CategoryPosition, write_only=True, required=False)

    class Meta:
        model = Category
        fields = ["parent", "target_id", "type_name", "position"]

    def validate(self, attrs):
        position = attrs.get("position", None)
        target_id = attrs.get("target_id", None)

        if target_id and (not Category.objects.filter(id=target_id).exists()):
            raise CategoryExceptions.NotFoundCategory()

        if (target_id is not None) and (position is None):
            raise CategoryExceptions.CategoryException(detail="target_id must be with position")

        return attrs

    def create(self, validated_data):
        target = None
        position = validated_data.pop("position", None)
        if target_id := validated_data.pop("target_id", None):
            target = Category.objects.get(id=target_id)

        with transaction.atomic():
            category = Category(**validated_data)
            if target and position:
                category.insert_at(target=target, position=position)
            category.save()
        return category


class ProductCreateRequestSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field="uuid")
    name = serializers.CharField()
    content = serializers.CharField(required=False)
    stock = serializers.IntegerField()
    initial_stock = serializers.IntegerField()
    price = serializers.IntegerField()
    selling = serializers.BooleanField(default=True)

    class Meta:
        model = Product
        fields = ["category", "name", "content", "stock", "initial_stock", "price", "selling"]
