from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.permissions import IsOwner

from .filters import NoteFilter
from .models import Note
from .serializers import NoteSerializer


@extend_schema_view(
    list=extend_schema(summary="Список заметок"),
    create=extend_schema(summary="Создать заметку"),
    retrieve=extend_schema(summary="Получить заметку"),
    update=extend_schema(summary="Обновить заметку"),
    partial_update=extend_schema(summary="Частично обновить заметку"),
    destroy=extend_schema(summary="Удалить заметку"),
)
@extend_schema(tags=["notes"])
class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_class = NoteFilter
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at", "title"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Note.objects.none()
        return Note.objects.filter(owner=self.request.user).select_related("owner")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def set_pinned(self, value):
        note = self.get_object()
        note.is_pinned = value
        note.save(update_fields=["is_pinned", "updated_at"])
        return Response(self.get_serializer(note).data)

    @extend_schema(summary="Закрепить заметку", request=None)
    @action(detail=True, methods=["post"])
    def pin(self, request, pk=None):
        return self.set_pinned(True)

    @extend_schema(summary="Открепить заметку", request=None)
    @action(detail=True, methods=["post"])
    def unpin(self, request, pk=None):
        return self.set_pinned(False)
