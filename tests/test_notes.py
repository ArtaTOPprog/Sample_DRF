import pytest

from apps.notes.models import Note
from tests.factories import make_note

pytestmark = pytest.mark.django_db

URL = "/api/v1/notes/"


def detail(note):
    return f"{URL}{note.id}/"


def test_notes_require_auth(api_client):
    assert api_client.get(URL).status_code == 401


def test_create_note_sets_owner(auth_client, user):
    response = auth_client.post(URL, {"title": "  Покупки  ", "content": "Хлеб"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Покупки"
    assert data["owner"] == user.username
    assert Note.objects.get(id=data["id"]).owner == user


def test_html_is_stored_as_is(auth_client):
    response = auth_client.post(URL, {"title": "<b>Жирный</b>", "content": "a & b"})
    assert response.json()["title"] == "<b>Жирный</b>"
    assert response.json()["content"] == "a & b"


def test_empty_title_is_rejected(auth_client):
    response = auth_client.post(URL, {"title": "   ", "content": "Текст"})
    assert response.status_code == 400
    assert "title" in response.json()


def test_list_shows_only_own_notes(auth_client, user, other_user):
    make_note(user, title="Моя")
    make_note(other_user, title="Чужая")
    data = auth_client.get(URL).json()
    assert data["count"] == 1
    assert data["results"][0]["title"] == "Моя"


def test_foreign_note_is_not_found(auth_client, other_user):
    note = make_note(other_user)
    assert auth_client.get(detail(note)).status_code == 404
    assert auth_client.patch(detail(note), {"title": "Взлом"}).status_code == 404
    assert auth_client.delete(detail(note)).status_code == 404
    note.refresh_from_db()
    assert note.title == "Заметка"


def test_partial_update(auth_client, user):
    note = make_note(user)
    response = auth_client.patch(detail(note), {"content": "Новый текст"})
    assert response.status_code == 200
    note.refresh_from_db()
    assert note.content == "Новый текст"
    assert note.title == "Заметка"


def test_full_update(auth_client, user):
    note = make_note(user)
    response = auth_client.put(detail(note), {"title": "Другой", "content": "Текст 2"})
    assert response.status_code == 200
    assert response.json()["title"] == "Другой"


def test_owner_cannot_be_changed(auth_client, user, other_user):
    note = make_note(user)
    auth_client.patch(detail(note), {"owner": other_user.id})
    note.refresh_from_db()
    assert note.owner == user


def test_delete(auth_client, user):
    note = make_note(user)
    assert auth_client.delete(detail(note)).status_code == 204
    assert not Note.objects.filter(id=note.id).exists()


def test_pin_and_unpin(auth_client, user):
    note = make_note(user)
    assert auth_client.post(f"{detail(note)}pin/").json()["is_pinned"] is True
    assert auth_client.post(f"{detail(note)}unpin/").json()["is_pinned"] is False


def test_pinned_notes_go_first(auth_client, user):
    make_note(user, title="Обычная")
    make_note(user, title="Важная", is_pinned=True)
    titles = [n["title"] for n in auth_client.get(URL).json()["results"]]
    assert titles == ["Важная", "Обычная"]


def test_filter_search_and_ordering(auth_client, user):
    make_note(user, title="Список покупок", is_archived=True)
    make_note(user, title="Идеи", content="Надо купить книгу")
    make_note(user, title="Альбом")

    archived = auth_client.get(URL, {"is_archived": "true"}).json()
    assert [n["title"] for n in archived["results"]] == ["Список покупок"]

    found = auth_client.get(URL, {"search": "куп"}).json()
    assert {n["title"] for n in found["results"]} == {"Список покупок", "Идеи"}

    ordered = auth_client.get(URL, {"ordering": "title"}).json()
    assert [n["title"] for n in ordered["results"]] == ["Альбом", "Идеи", "Список покупок"]


def test_pagination(auth_client, user):
    for i in range(5):
        make_note(user, title=f"Заметка {i}")
    data = auth_client.get(URL, {"page_size": 2, "page": 2}).json()
    assert data["count"] == 5
    assert len(data["results"]) == 2
    assert data["next"] and data["previous"]


def test_not_found_has_code(auth_client):
    response = auth_client.get(f"{URL}999999/")
    assert response.status_code == 404
    assert response.json()["code"] == "not_found"
