import pytest
from django.urls import reverse
from rest_framework import status

from orders.services import order_service


@pytest.fixture
def order_data(user, product_set):
    product1 = product_set[0]
    product2 = product_set[1]
    product_data = [
        {
            "product_id": product1.id,
            "product_name": product1.name,
            "category_name": product1.category.type_name,
            "quantity": 2,
            "price": product1.price,
        },
        {
            "product_id": product2.id,
            "product_name": product2.name,
            "category_name": product2.category.type_name,
            "quantity": 10,
            "price": product2.price,
        },
    ]
    return {
        "user": user,
        "status": 1,
        "shipping_address": "test address",
        "detail_shipping_address": "test detail address",
        "product_orders": product_data
    }


@pytest.fixture
def order(order_data):
    order_dto = order_service.create_order_dto(order_data)
    product_order_dto_list = order_service.create_product_order_dto_list(order_data["product_orders"])
    return order_service.order(order_dto, product_order_dto_list)


@pytest.mark.django_db
def test_주문_생성(user, authenticated_client, order_data, product_set):
    # case
    order_data.pop("user")
    product1 = product_set[0]
    product2 = product_set[1]

    old_product_1_quantity = product1.stock
    old_product_2_quantity = product2.stock
    product_1_purchase_quantity = order_data["product_orders"][0]["quantity"]
    product_2_purchase_quantity = order_data["product_orders"][1]["quantity"]

    # when
    url = reverse("orders:order_list_create")
    response = authenticated_client.post(url, data=order_data, format="json")

    # then
    assert response.status_code == status.HTTP_201_CREATED

    # 총 가격 확인
    expected_total_price = sum(each["price"] * each["quantity"] for each in order_data["product_orders"])
    assert response.data["total_price"] == expected_total_price
    # 제품 수량 확인
    product1.refresh_from_db()
    product2.refresh_from_db()
    after_saved_quantities = [product1.stock, product2.stock]
    expected_quantity = [old_product_1_quantity - product_1_purchase_quantity,
                         old_product_2_quantity - product_2_purchase_quantity]
    assert after_saved_quantities == expected_quantity


@pytest.mark.django_db
def test_기존_주문수량보다_많은값으로_수정(authenticated_client, product_set, order):
    # case
    product_order = order.product_order_set.first()
    before_product_order_quantity = product_order.quantity
    before_product_stock = product_order.product.stock

    assert before_product_order_quantity == 2
    assert before_product_stock == 18
    update_quantity = 3

    # when
    url = reverse("orders:order_quantity_update", kwargs={"uuid": product_order.uuid})
    data = {"quantity": update_quantity}
    response = authenticated_client.put(url, data=data, format="json")

    # then
    assert response.status_code == status.HTTP_200_OK

    # 업데이트 후 product_order.quantity, product.stock 수량 확인
    product_order.refresh_from_db()
    after_product_order_quantity = product_order.quantity
    after_product_stock = product_order.product.stock

    assert after_product_order_quantity == update_quantity
    assert after_product_stock == before_product_stock - (update_quantity - before_product_order_quantity)


@pytest.mark.django_db
def test_기존_주문수량보다_적은값으로_수정(authenticated_client, product_set, order):
    # case
    product_order = order.product_order_set.first()
    before_product_order_quantity = product_order.quantity
    before_product_stock = product_order.product.stock

    assert before_product_order_quantity == 2
    assert before_product_stock == 18
    update_quantity = 1

    # when
    url = reverse("orders:order_quantity_update", kwargs={"uuid": product_order.uuid})
    data = {"quantity": update_quantity}
    response = authenticated_client.put(url, data=data, format="json")

    # then
    assert response.status_code == status.HTTP_200_OK

    # 업데이트 후 product_order.quantity, product.stock 수량 확인
    product_order.refresh_from_db()
    after_product_order_quantity = product_order.quantity
    after_product_stock = product_order.product.stock

    assert after_product_order_quantity == update_quantity
    assert after_product_stock == before_product_stock + (before_product_order_quantity - update_quantity)
