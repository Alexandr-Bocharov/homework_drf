from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserUpdateAPIView, UserListAPIView, UserRetrieveAPIView

app_name = UsersConfig.name


urlpatterns = [
    path("", UserListAPIView.as_view(), name='user_list'),
    path("create/", UserCreateAPIView.as_view(), name='user_create'),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name='user_update'),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name='user_view'),
]
