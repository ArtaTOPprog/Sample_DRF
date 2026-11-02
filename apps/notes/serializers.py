from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Note
        fields = ["id", "owner", "title", "content", "is_pinned", "is_archived", "created_at", "updated_at"]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Заголовок не может быть пустым.")
        return value

    def validate_content(self, value):
        return value.strip()
