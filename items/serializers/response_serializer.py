from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from items.models import Category, Product


class CategoryListResponseSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "type_name", "children"]

    @extend_schema_field({"type": "object", "example": [{"id": 1, "type_name": "string", "children": []}]})
    def get_children(self, instance):
        return CategoryListResponseSerializer(instance=instance.get_children(), many=True).data


class ProductResponseSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    name = serializers.CharField()
    content = serializers.CharField()
    stock = serializers.IntegerField()
    initial_stock = serializers.IntegerField()
    price = serializers.IntegerField()
    selling = serializers.BooleanField()

    class Meta:
        model = Product
        fields = ["category", "name", "content", "stock", "initial_stock", "price", "selling"]
