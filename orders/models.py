import uuid

from django.conf import settings
from django.db import models

from commons.models import CommonModel
from items.models import Product


class OrderStatus(models.IntegerChoices):
    ORDERED = 1, "주문 시작"
    PAID = 2, "결제 완료"
    SHIPPING = 3, "배송중"
    DELIVERED = 4, "배송 완료"


class Order(CommonModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.ORDERED)
    shipping_address = models.CharField(max_length=255, null=True, blank=True)
    detail_shipping_address = models.BinaryField()
    total_price = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user_id", "-created_at"], name="user__created_at_desc_idx"),
            models.Index(fields=["-created_at"], name="created_at_desc_index"),
        ]

    def is_available_to_update(self):
        return bool(self.status < OrderStatus.PAID)


class ProductOrder(CommonModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name="product_order_set")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="product_order_set")
    category_name = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    quantity = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["order_id", "-created_at"], name="order__created_at_desc_idx")
        ]
        constraints = [
            models.UniqueConstraint(fields=["order_id", "product_id"], name="unique_order_product_id")
        ]
