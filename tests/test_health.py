import pytest


@pytest.mark.django_db
def test_health(api_client):
    response = api_client.get("/api/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


@pytest.mark.django_db
def test_schema_is_available(api_client):
    response = api_client.get("/api/schema/")
    assert response.status_code == 200
    assert b"/api/v1/notes/" in response.content


@pytest.mark.django_db
def test_docs_are_available(api_client):
    assert api_client.get("/api/docs/").status_code == 200
    assert api_client.get("/api/redoc/").status_code == 200
