import pytest
from django.urls import reverse
from rest_framework import status

from items.models import Category
from items.tests.fixtures import category_set


@pytest.mark.django_db
def test_카테고리_리스트_확인(category_set, authenticated_client):
    """
    fixture category 구조
    - root1
        - root1_child1
        - root1_child2
            - root1_child2_child1
        - root1_child3
    - root2
    """
    # api 응답 테스트
    url = reverse("items:category_list_create")
    response = authenticated_client.get(url)
    root_node_count = len(response.data)

    assert response.status_code == status.HTTP_200_OK
    assert root_node_count == 2

    # db vs response 비교 테스트
    # queryset node
    root1 = category_set[0]
    root1_children = root1.get_children()
    # response node
    root1_from_response = response.data[0]
    root1_children_from_response = root1_from_response["children"]

    for index, child in enumerate(root1_children):
        assert child.type_name == root1_children_from_response[index]["type_name"]


@pytest.mark.parametrize("input_data, error_message, status_code", [
    ({"type_name": "추가 카테고리", "position": "right"},
     None, status.HTTP_201_CREATED),
    ({"type_name": "추가 카테고리", "position": "invalid_position"},
     'position: "invalid_position"이 유효하지 않은 선택(choice)입니다.',
     status.HTTP_400_BAD_REQUEST),
])
@pytest.mark.django_db
def test_카테고리_생성(authenticated_client, input_data, error_message, status_code):
    # case
    url = reverse("items:category_list_create")

    # when
    response = authenticated_client.post(url, input_data, format="json")
    result = response.json()

    # then
    assert response.status_code == status_code
    if response.status_code != status.HTTP_201_CREATED:
        assert result["targets"][0]["msg"] == error_message


@pytest.mark.django_db
def test_카테고리_생성_후_순서_확인(category_set, authenticated_client):
    """
    - root1
        - root1_child1
        - ["추가 카테고리"]
        - root1_child2
            - root1_child2_child1
        - root1_child3
    - root2
    """
    # case: 기존 카테고리 리스트
    root1 = category_set[0]
    # assert root1.is_root_node()
    children = root1.get_children()
    root1_child1 = children.first()

    # when
    url = reverse("items:category_list_create")
    create_response = authenticated_client.post(url, {
        "type_name": "추가 카테고리",
        "target_id": root1_child1.id,
        "position": "right",
    }, format="json")

    # then: 변경된 카테고리 순서 확인
    assert create_response.status_code == status.HTTP_201_CREATED

    expected_data = ["root1_child1", "추가 카테고리", "root1_child2", "root1_child3"]

    root1 = Category.objects.first()
    for index, category in enumerate(root1.get_children()):
        assert category.type_name == expected_data[index]


@pytest.mark.django_db
def test_카테고리_업데이트(authenticated_client):
    # case
    changed_name = "변경된 카테고리"
    first_category = Category.objects.create(type_name="첫번째 카테고리", tree_id=1, level=0)
    _ = Category.objects.create(type_name="두번째 카테고리", tree_id=2, level=0)

    # when
    url = reverse("items:category_update_name", kwargs={"pk": first_category.pk})
    response = authenticated_client.put(url, {"type_name": changed_name}, format="json")

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.data["type_name"] == changed_name


@pytest.mark.django_db
def test_카테고리_위치_업데이트(authenticated_client):
    # case: 순서 확인
    first_category = Category.objects.create(type_name="첫번째 카테고리", tree_id=1, level=0)
    second_category = Category.objects.create(type_name="두번째 카테고리", tree_id=2, level=0)
    assert first_category.get_next_sibling() == second_category

    # when
    url = reverse("items:category_update_position", kwargs={"pk": second_category.id})
    _ = authenticated_client.put(url, {"target_id": first_category.id, "position": "left"}, format="json")

    # then
    first_category.refresh_from_db()
    second_category.refresh_from_db()
    assert first_category.get_next_sibling() != second_category
    assert second_category.get_next_sibling() == first_category
