from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    ChangePasswordSerializer,
    LogoutSerializer,
    RegisterResponseSerializer,
    RegisterSerializer,
    TokenPairSerializer,
    UserSerializer,
)


@extend_schema(tags=["auth"])
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(summary="Регистрация", responses={201: RegisterResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {"user": UserSerializer(user).data, "tokens": TokenPairSerializer.for_user(user)}
        return Response(data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["auth"])
class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "options", "head"]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["auth"])
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Смена пароля", request=ChangePasswordSerializer, responses={204: None})
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["auth"])
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Выход (refresh-токен в чёрный список)", request=LogoutSerializer, responses={204: None})
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            RefreshToken(serializer.validated_data["refresh"]).blacklist()
        except TokenError:
            return Response({"detail": "Токен недействителен.", "code": "token_not_valid"}, status=400)
        return Response(status=status.HTTP_204_NO_CONTENT)
