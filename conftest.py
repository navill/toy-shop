import os

import pytest
from rest_framework.test import APIClient

from users.models import User
from users.services import user_service, UserDTO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
pytest_plugins = [
    "items.tests.fixtures",
]


@pytest.fixture
def user_data():
    return {
        "username": "홍길동",
        "email": "hong@fixture.com",
        "password": "test1234",
        "nickname": "fixture_hong",
        "phone": "01011112222",
        "address": "서울 어딘가"
    }


@pytest.fixture
def user_dto(user_data):
    return user_service.get_user_dto(**user_data)


@pytest.fixture
def user(user_dto):
    return user_service.join(user_dto)


@pytest.fixture
def other_user():
    data = {
        "username": "김춘향",
        "email": "kim@fixture.com",
        "password": "test1234",
        "nickname": "fixture_kim",
        "phone": "01012344321",
        "address": "경기 어딘가"
    }
    dto = user_service.get_user_dto(**data)
    return user_service.join(dto)


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client
