from django.db import transaction
from rest_framework import serializers

from items.exceptions import ProductExceptions
from orders.models import ProductOrder, Order, OrderStatus
from orders.services import order_service


class ProductOrderCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    category_name = serializers.CharField()
    product_name = serializers.CharField()
    price = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = ProductOrder
        fields = ["category_name", "product_id", "product_name", "price", "quantity"]


class OrderCreateRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=True)
    shipping_address = serializers.CharField()
    detail_shipping_address = serializers.CharField()
    product_orders = ProductOrderCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["user", "status", "shipping_address", "detail_shipping_address", "product_orders"]

    def create(self, validated_data: dict) -> Order:
        order_dto = order_service.create_order_dto(validated_data)
        product_order_dto_list = order_service.create_product_order_dto_list(validated_data["product_orders"])
        return order_service.order(order_dto, product_order_dto_list)


class OrderUpdateRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=True)
    status = serializers.ChoiceField(choices=OrderStatus.choices, required=False)
    shipping_address = serializers.CharField(required=False)
    detail_shipping_address = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = ["user", "status", "shipping_address", "detail_shipping_address"]

    def update(self, instance, validated_data):
        order_dto = order_service.create_order_dto(validated_data)
        return super().update(instance, order_dto.dict(exclude_none=True))


class ProductOrderUpdateRequestSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = ProductOrder
        fields = ["quantity"]

    def update(self, instance: ProductOrder, validated_data: dict) -> ProductOrder:
        try:
            with transaction.atomic():
                order_service.update_quantity(instance, validated_data["quantity"])
                return super().update(instance, validated_data)
        except Exception as e:
            raise ProductExceptions.ProductException(detail=e)
