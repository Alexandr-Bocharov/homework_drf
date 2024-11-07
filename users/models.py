from django.db import models
from django.contrib.auth.models import AbstractUser


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="почта")

    phone = models.CharField(max_length=50, verbose_name="телефон", **NULLABLE)
    city = models.CharField(max_length=50, verbose_name="город", **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars/", verbose_name="аватар", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
