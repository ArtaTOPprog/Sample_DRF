from django.urls import path
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import ChangePasswordView, LogoutView, MeView, RegisterView

app_name = "users"

auth_tag = extend_schema_view(post=extend_schema(tags=["auth"]))

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", auth_tag(TokenObtainPairView).as_view(), name="token"),
    path("token/refresh/", auth_tag(TokenRefreshView).as_view(), name="token-refresh"),
    path("token/verify/", auth_tag(TokenVerifyView).as_view(), name="token-verify"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
