from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet
from django.urls import path
from materials.views import (
    LessonListAPIView,
    LessonCreateAPIView,
    LessonUpdateAPIView,
    LessonRetrieveAPIView,
    LessonDestroyAPIView,
)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name='lesson_list'),
    path("lessons/create/", LessonCreateAPIView.as_view(), name='lesson_create'),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name='lesson_update'),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name='lesson_delete'),
              ] + router.urls
