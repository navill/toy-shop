from rest_framework import serializers

from commons.serializer_fields import DecryptedSerializerField
from orders.models import ProductOrder, Order


class ProductOrderCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    category_name = serializers.CharField()
    product_name = serializers.CharField()
    price = serializers.CharField()
    quantity = serializers.IntegerField()

    class Meta:
        model = ProductOrder
        fields = ["category_name", "product_id", "product_name", "price", "quantity"]


class OrderResponseSerializer(serializers.ModelSerializer):
    detail_shipping_address = DecryptedSerializerField()
    products = ProductOrderCreateSerializer(many=True, read_only=True, source="product_order_set")

    class Meta:
        model = Order
        fields = ["uuid", "status", "shipping_address", "detail_shipping_address", "total_price", "products"]


class ProductOrderUpdateResponseSerializer(serializers.ModelSerializer):
    product_stock = serializers.IntegerField(source="product.stock")

    class Meta:
        model = ProductOrder
        fields = ["uuid", "quantity", "product_stock"]
