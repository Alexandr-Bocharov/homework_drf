from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    UserUpdateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    PaymentListAPIView,
    PaymentCreateAPIView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("", UserListAPIView.as_view(), name="user_list"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user_view"),
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
