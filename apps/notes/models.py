from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class Note(TimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name="Автор",
    )
    title = models.CharField("Заголовок", max_length=200)
    content = models.TextField("Содержание", max_length=10000, blank=True)
    is_pinned = models.BooleanField("Закреплена", default=False)
    is_archived = models.BooleanField("В архиве", default=False)

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        ordering = ["-is_pinned", "-created_at"]
        indexes = [models.Index(fields=["owner", "-created_at"])]

    def __str__(self):
        return self.title[:50]
