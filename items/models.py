import uuid

import funcy
from concurrency.exceptions import RecordModifiedError
from concurrency.fields import IntegerVersionField
from django.db import models, IntegrityError, router
from django.db.models import F
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from commons.models import CommonModel, MetaDateModel
from items.exceptions import ProductExceptions


class CategoryPosition(models.TextChoices):
    FIRST_CHILD = "first-child", "first-child"
    LAST_CHILD = "last-child", "last-child"
    LEFT = "left", "left"
    RIGHT = "right", "right"


class Category(MetaDateModel, MPTTModel):
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    type_name = models.CharField(max_length=100)

    class MPTTMeta:
        level_attr = 'level'

    def __str__(self):
        return self.type_name


class Product(CommonModel):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    initial_stock = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    selling = models.BooleanField(default=True)
    version = IntegerVersionField()

    class Meta:
        indexes = [
            models.Index(fields=["-deleted_at", "-created_at", "selling"], name="prod_selling_idx"),
            models.Index(fields=["-deleted_at", "category", "-created_at"], name="prod_as_category_idx")
        ]
        ordering = ["-created_at"]

    @funcy.retry(5, errors=RecordModifiedError, timeout=5)
    def decrease_stock(self, quantity: int = 1, save: bool = True) -> None:
        self.stock = F("stock") - quantity
        if save:
            try:
                self.save()
                self.refresh_from_db(using=router.db_for_write(self))
            except IntegrityError:
                raise ProductExceptions.OutOfStockException()

    @funcy.retry(5, errors=RecordModifiedError, timeout=5)
    def increase_stock(self, quantity: int = 1, save: bool = True) -> None:
        self.stock = F("stock") + quantity
        if save:
            self.save()
            self.refresh_from_db(using=router.db_for_write(self))

    def is_available(self) -> bool:
        return self.selling

    def validate_stock(self, quantity: int) -> bool:
        if self.stock == quantity:
            return False

        if self.stock < quantity:
            raise ProductExceptions.OutOfStockException()

        if (self.stock + quantity) > self.initial_stock:
            raise ProductExceptions.OverStockException()

        return True
