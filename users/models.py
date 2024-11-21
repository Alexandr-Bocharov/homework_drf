from django.db import models
from django.contrib.auth.models import AbstractUser
from materials.models import Course, Lesson
from utils import NULLABLE
from datetime import datetime


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


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "cash", "наличные"
        TRANSFER_TO_ACCOUNT = "transfer_to_account", "перевод на счет"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь"
    )
    payment_date = models.DateField(verbose_name="дата оплаты")
    paid_course = models.ForeignKey(
        Course, verbose_name="Оплаченный курс", on_delete=models.SET_NULL, **NULLABLE
    )
    paid_lesson = models.ForeignKey(
        Lesson, verbose_name="Оплаченный урок", on_delete=models.SET_NULL, **NULLABLE
    )
    payment_amount = models.PositiveIntegerField(verbose_name="сумма оплаты")
    payment_method = models.CharField(
        max_length=20, verbose_name="способ оплаты", choices=PaymentMethod.choices
    )

    def __str__(self):
        return f"{self.paid_course if self.paid_course else self.paid_lesson} - оплачен"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
