from django.contrib.auth import get_user_model

from apps.notes.models import Note


def make_user(username, password="S3cure-pass-123", **extra):
    extra.setdefault("email", f"{username}@example.com")
    return get_user_model().objects.create_user(username=username, password=password, **extra)


def make_note(owner, **extra):
    extra.setdefault("title", "Заметка")
    extra.setdefault("content", "Текст")
    return Note.objects.create(owner=owner, **extra)
