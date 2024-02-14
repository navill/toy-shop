import random

import pytest

from items.models import Category, Product


@pytest.fixture
def category_set():
    """
    fixture category 구조
    - r1
        - r1_c1
        - r1_c2
            - r1_c2_c1
        - r1_c3
    - r2
    """
    r1 = Category.objects.create(type_name="root1")
    Category.objects.create(type_name="root2")

    r1_c1 = Category(type_name="root1_child1", parent=r1)
    r1_c1.insert_at(target=r1, position="first-child", save=True)

    r1_c2 = Category(type_name="root1_child2", parent=r1)
    r1_c2.insert_at(target=r1_c1, position="right", save=True)

    r1_c3 = Category(type_name="root1_child3", parent=r1)
    r1_c3.insert_at(target=r1, position="last-child", save=True)

    r1_c2_c1 = Category(type_name="roo1_child2_child1", parent=r1)
    r1_c2_c1.insert_at(target=r1_c2, position="first-child", save=True)
    return Category.objects.get_cached_trees()


@pytest.fixture
def product_set(category_set):
    product_list = list()
    for category in Category.objects.all():
        for index in range(0, 10):
            product = Product.objects.create(
                category=category,
                name=f"item-{index}",
                content=f"item number is {index}",
                stock=20,
                initial_stock=30,
                price=random.randrange(5000, 100000, 1000),
                selling=True
            )
            product_list.append(product)
    return product_list
