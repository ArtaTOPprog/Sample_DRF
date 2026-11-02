import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_register_returns_user_and_tokens(api_client, password):
    response = api_client.post(
        "/api/v1/auth/register/",
        {"username": "anna", "email": "Anna@Example.com", "password": password},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["username"] == "anna"
    assert data["user"]["email"] == "anna@example.com"
    assert "password" not in data["user"]
    assert {"access", "refresh"} <= data["tokens"].keys()
    assert User.objects.get(username="anna").check_password(password)


def test_register_rejects_weak_password(api_client):
    response = api_client.post(
        "/api/v1/auth/register/", {"username": "anna", "email": "anna@example.com", "password": "123"}
    )
    assert response.status_code == 400
    assert "password" in response.json()


def test_register_rejects_duplicate_email(api_client, user, password):
    response = api_client.post(
        "/api/v1/auth/register/",
        {"username": "other", "email": user.email.upper(), "password": password},
    )
    assert response.status_code == 400
    assert "email" in response.json()


def test_token_refresh_and_verify(api_client, user, password):
    tokens = api_client.post("/api/v1/auth/token/", {"username": user.username, "password": password}).json()
    assert api_client.post("/api/v1/auth/token/verify/", {"token": tokens["access"]}).status_code == 200
    refreshed = api_client.post("/api/v1/auth/token/refresh/", {"refresh": tokens["refresh"]})
    assert refreshed.status_code == 200
    assert "access" in refreshed.json()


def test_wrong_password_is_rejected(api_client, user):
    response = api_client.post("/api/v1/auth/token/", {"username": user.username, "password": "wrong"})
    assert response.status_code == 401


def test_me_requires_auth(api_client):
    response = api_client.get("/api/v1/auth/me/")
    assert response.status_code == 401
    assert response.json()["code"] == "not_authenticated"


def test_me_with_bearer_token(api_client, user, password):
    access = api_client.post("/api/v1/auth/token/", {"username": user.username, "password": password}).json()["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    response = api_client.get("/api/v1/auth/me/")
    assert response.status_code == 200
    assert response.json()["username"] == user.username


def test_me_update(auth_client, user):
    response = auth_client.patch("/api/v1/auth/me/", {"first_name": "Иван", "username": "hacker"})
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.first_name == "Иван"
    assert user.username == "ivan"


def test_me_put_is_not_allowed(auth_client):
    assert auth_client.put("/api/v1/auth/me/", {"first_name": "Иван"}).status_code == 405


def test_change_password(auth_client, user, password):
    response = auth_client.post(
        "/api/v1/auth/change-password/", {"old_password": password, "new_password": "N3w-strong-pass"}
    )
    assert response.status_code == 204
    user.refresh_from_db()
    assert user.check_password("N3w-strong-pass")


def test_change_password_with_wrong_old_password(auth_client):
    response = auth_client.post(
        "/api/v1/auth/change-password/", {"old_password": "wrong", "new_password": "N3w-strong-pass"}
    )
    assert response.status_code == 400
    assert "old_password" in response.json()


def test_logout_blacklists_refresh_token(api_client, user, password):
    tokens = api_client.post("/api/v1/auth/token/", {"username": user.username, "password": password}).json()
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    assert api_client.post("/api/v1/auth/logout/", {"refresh": tokens["refresh"]}).status_code == 204
    response = api_client.post("/api/v1/auth/token/refresh/", {"refresh": tokens["refresh"]})
    assert response.status_code == 401


def test_logout_with_invalid_token(auth_client):
    response = auth_client.post("/api/v1/auth/logout/", {"refresh": "broken"})
    assert response.status_code == 400
