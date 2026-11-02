import pytest
from rest_framework.test import APIClient

from tests.factories import make_user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def password():
    return "S3cure-pass-123"


@pytest.fixture
def user(db, password):
    return make_user("ivan", password=password)


@pytest.fixture
def other_user(db, password):
    return make_user("petr", password=password)


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client
