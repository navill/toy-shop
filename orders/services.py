from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from pydantic import BaseModel

from commons.deidentifications import pi_cipher
from items.exceptions import ProductExceptions
from items.models import Product
from orders.exceptions import OrderExceptions
from orders.models import Order, ProductOrder

User = get_user_model()


class ProductOrderDTO(BaseModel):
    product_id: int
    product_name: str
    category_name: str
    price: int
    quantity: int


class OrderDTO(BaseModel):
    user: User
    status: Optional[int] = None
    shipping_address: Optional[str] = None
    detail_shipping_address: Optional[bytes] = None
    total_price: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True


class OrderService:
    def order(self, order_dto: OrderDTO, product_order_dto_list: list[ProductOrderDTO]) -> Order:
        order_dto.total_price = self.calculate_total_price(product_order_dto_list)
        with transaction.atomic():
            order = self.create_order(order_dto)
            self.create_product_order(order, product_order_dto_list)
            self.decrease_products_quantity(product_order_dto_list)
        return order

    def create_order(self, dto: OrderDTO):
        return Order.objects.create(
            user=dto.user,
            status=dto.status,
            total_price=dto.total_price,
            shipping_address=dto.shipping_address,
            detail_shipping_address=dto.detail_shipping_address
        )

    def create_product_order(self, order: Order, dto_list: list[ProductOrderDTO]) -> None:
        try:
            product_orders = [
                ProductOrder(
                    order=order,
                    product_id=dto.product_id,
                    product_name=dto.product_name,
                    category_name=dto.category_name,
                    price=dto.price,
                    quantity=dto.quantity
                ) for dto in dto_list]
            ProductOrder.objects.bulk_create(product_orders)
        except Exception as e:
            raise OrderExceptions.OrderException(detail="주문 제품 기록 실패") from e

    def decrease_products_quantity(self, product_order_dto_list: list[ProductOrderDTO]) -> None:
        try:
            product_order_data = {product.product_id: product.quantity for product in product_order_dto_list}
            queryset = Product.objects.filter(id__in=list(product_order_data.keys()))
            for product in queryset:
                if product.is_available():
                    product.decrease_stock(quantity=product_order_data[product.id])
                else:
                    raise ProductExceptions.ProductException(detail=f"{product.name}-판매 중단 제품")
        except ProductExceptions.OutOfStockException:
            raise
        except Exception as e:
            raise ProductExceptions.ProductException(detail="제품 수량 업데이트 실패") from e

    def calculate_total_price(self, product_dto_list: list[ProductOrderDTO]) -> int:
        return sum(dto.price * dto.quantity for dto in product_dto_list)

    def create_order_dto(self, validated_data: dict) -> OrderDTO:
        address = validated_data.get("detail_shipping_address", None)
        detail_shipping_address = pi_cipher.encrypt(address) if address else None

        return OrderDTO(
            user=validated_data.get("user"),
            status=validated_data.get("status"),
            shipping_address=validated_data.get("shipping_address"),
            detail_shipping_address=detail_shipping_address
        )

    def create_product_order_dto_list(self, validated_data: list[dict]) -> list[ProductOrderDTO]:
        return [self.create_product_order_dto(**data) for data in validated_data]

    def create_product_order_dto(self, **validated_data: dict) -> ProductOrderDTO:
        return ProductOrderDTO(
            product_id=validated_data["product_id"],
            product_name=validated_data["product_name"],
            category_name=validated_data["category_name"],
            price=validated_data["price"],
            quantity=validated_data["quantity"]
        )

    def update_quantity(self, product_order, quantity: int):
        saved_quantity = product_order.quantity
        product = product_order.product
        if product.validate_stock(quantity):
            if saved_quantity > quantity:
                product.increase_stock(saved_quantity - quantity)
            elif saved_quantity < quantity:
                product.decrease_stock(quantity - saved_quantity)


order_service = OrderService()
