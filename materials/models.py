from django.db import models
from django.conf import settings

from utils import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="название")
    preview = models.ImageField(
        upload_to="materials/courses_previews/", verbose_name="превью", **NULLABLE
    )
    description = models.TextField(verbose_name="описание", **NULLABLE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, verbose_name="курс", on_delete=models.CASCADE, **NULLABLE
    )
    name = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(verbose_name="описание", **NULLABLE)
    preview = models.ImageField(
        upload_to="materials/lessons_previews/", verbose_name="превью", **NULLABLE
    )
    link = models.CharField(max_length=250, verbose_name="ссылка", **NULLABLE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Subscription(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"Подписка на курс: {self.course.name} для {self.owner}"

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
