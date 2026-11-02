from django.db import connection
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = []

    @extend_schema(
        tags=["health"],
        summary="Проверка работоспособности",
        responses=inline_serializer(
            "Health",
            fields={"status": serializers.CharField(), "database": serializers.CharField()},
        ),
    )
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            database = "ok"
        except Exception:
            database = "unavailable"
        healthy = database == "ok"
        return Response(
            {"status": "ok" if healthy else "error", "database": database},
            status=status.HTTP_200_OK if healthy else status.HTTP_503_SERVICE_UNAVAILABLE,
        )
