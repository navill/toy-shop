import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken


@pytest.mark.parametrize("data, status_code", [
    ({
         "email": "test1@test.com",
         "password": "test1234",
         "phone": "01012345678",
         "username": "홍길동",
         "nickname": "hong"
     }, status.HTTP_201_CREATED),
    ({
         "email": "test1@test.com",
         "password": "test1234",
         "phone": None,
         "username": "홍길동",
         "nickname": "hong"
     }, status.HTTP_400_BAD_REQUEST),
    ({
         "email": "test1@test.com",
         "password": "test1234",
         "phone": "01012345678",
         "username": None,
         "nickname": "hong"
     }, status.HTTP_400_BAD_REQUEST),
    ({
         "email": "test1@test.com",
         "password": "test1234",
         "phone": "01012345678",
         "username": "홍길동",
         "nickname": None
     }, status.HTTP_400_BAD_REQUEST),
])
@pytest.mark.django_db
def test_유저_생성(api_client, data, status_code):
    url = reverse("users:join")
    response = api_client.post(url, data, format="json")

    assert response.status_code == status_code
    if response.status_code == status.HTTP_201_CREATED:
        response_data = response.data
        for masked_field in ["username", "phone"]:
            assert "*" in response_data[masked_field]


@pytest.mark.django_db
def test_인증_토큰_발급(user_data, user, api_client):
    # case
    url = reverse("users:login")
    data = {"email": user_data["email"], "password": user_data["password"]}

    # when
    response = api_client.post(url, data, format="json")
    token = AccessToken(token=response.data["access"])

    # then
    assert response.status_code == status.HTTP_200_OK
    assert token["user_id"] == user.id


@pytest.mark.django_db
def test_유저_정보_접근(user, authenticated_client):
    # case
    url = reverse("users:retrieve", kwargs={"uuid": user.uuid})

    # when
    retrieve_response = authenticated_client.get(url)
    response_data = retrieve_response.data

    # then: 마스킹 확인
    assert retrieve_response.status_code == status.HTTP_200_OK
    for masked_field in ["username", "phone"]:
        assert "*" in response_data[masked_field]


@pytest.mark.django_db
def test_마스킹없는_유저_정보_접근(user, authenticated_client):
    # case
    url = reverse("users:retrieve", kwargs={"uuid": user.uuid})

    # when
    origin_response = authenticated_client.get(f"{url}?unmask=true")
    response_data = origin_response.data

    # then: 마스킹 포함 확인
    assert origin_response.status_code == status.HTTP_200_OK
    for masked_field in ["username", "phone"]:
        assert "*" in response_data[masked_field]


@pytest.mark.django_db
def test_다른유저_정보_접근(user, other_user, api_client):
    # case
    user_url = reverse("users:retrieve", kwargs={"uuid": user.uuid})
    # 다른 사용자 인증
    api_client.force_authenticate(user=other_user)

    # when
    retrieve_response = api_client.get(user_url)

    # then
    assert retrieve_response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_미인증_유저_정보_접근(user, api_client):
    url = reverse("users:retrieve", kwargs={"uuid": user.uuid})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
