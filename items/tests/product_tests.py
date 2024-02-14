import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_제품_리스트(authenticated_client, product_set):
    url = reverse("items:product_list_create")
    response = authenticated_client.get(url)

    assert len(response.data) == len(product_set)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_제품생성(authenticated_client, category_set):
    url = reverse("items:product_list_create")
    category = category_set[0]
    data = {
        "category": category.uuid,
        "name": "test_item",
        "content": "test_content",
        "quantity": 100,
        "price": 100_000,
        "selling": True
    }
    response = authenticated_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    for key, value in data.items():
        if key == "category":
            assert response.data.get(key) == category.type_name
        else:
            assert response.data.get(key) == value


@pytest.mark.django_db
def test_제품_수정(authenticated_client, category_set, product_set):
    # case
    product = product_set[0]
    other_category = category_set[1]
    expected_data = {
        "category": other_category.uuid,
        "name": "update_name",
        "content": "update_content",
        "quantity": 100,
        "initial_quantity": 100,
        "price": 100_000
    }
    # when
    url = reverse("items:product_update", kwargs={"pk": product.id})
    response = authenticated_client.put(url, data=expected_data, format="json")

    # then
    assert response.status_code == status.HTTP_200_OK
    for key, value in expected_data.items():
        assert response.data[key] == expected_data[key]
