from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
    ToggleSubscriptionSerializer,
)
from materials.models import Course, Lesson, Subscription
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from materials.paginators import CustomPaginator
from materials.tasks import send_message_about_update

from users.permissions import IsModer, IsOwner
from django.utils import timezone
from datetime import timedelta


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPaginator

    def get_permissions(self):
        # Настройка разрешений для каждого действия
        if self.action == "destroy":
            self.permission_classes = (IsAuthenticated, ~IsModer | IsOwner)
        elif self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner)
        elif self.action == "create":
            self.permission_classes = (IsAuthenticated, ~IsModer)

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Проверяет, является ли запрос PATCH
        instance = self.get_object()  # Получает объект для обновления
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        course_name = instance.name
        send_message_about_update.delay(course_name)
        self.perform_update(serializer)
        return Response(serializer.data)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPaginator


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~IsModer)

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        created_object = serializer.save()
        dt_now = timezone.now()
        print((dt_now - serializer.validated_data['course'].updated_at) >= timedelta(hours=4))
        # если у урока указан курс, тогда осуществляем рассылку тем, кто на нее подписан
        if serializer.validated_data['course'] and (
                dt_now - serializer.validated_data['course'].updated_at) >= timedelta(hours=4):
            course_id, lesson_id = serializer.validated_data['course'].pk, created_object.pk
            send_message_about_update.delay(course_id, lesson_id)
            serializer.validated_data['course'].updated_at = dt_now
            serializer.validated_data['course'].save()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | IsModer)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | IsModer)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Проверяет, является ли запрос PATCH
        instance = self.get_object()  # Получает объект для обновления
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        dt_now = timezone.now()
        # если у урока указан курс, тогда осуществляем рассылку тем, кто на нее подписан
        if instance.course and (dt_now - instance.course.updated_at) >= timedelta(hours=4):
            course_id, lesson_id = instance.course.pk, instance.id
            send_message_about_update.delay(course_id, instance.id)
            instance.course.updated_at = dt_now
            instance.course.save()

        self.perform_update(serializer)
        return Response(serializer.data)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~IsModer | IsOwner)


# class SubscriptionViewSet(viewsets.ModelViewSet):
#     serializer_class = SubscriptionSerializer
#     queryset = Subscription.objects.all()
#
#     def post(self, *args, **kwargs):
#         user = self.request.user
#         course_id = self.request.data.get('course_id')
#         course_item = get_object_or_404(Course, id=course_id)
#
#         subs_item = Subscription.objects.get(owner=user, course=course_item)
#
#         # Если подписка у пользователя на этот курс есть - удаляем ее
#         if subs_item.exists():
#             course_item.is_sub = False
#             message = 'подписка удалена'
#         # Если подписки у пользователя на этот курс нет - создаем ее
#         else:
#             course_item.is_sub = True
#             message = 'подписка добавлена'
#         # Возвращаем ответ в API
#         return Response({"message": message})


class ToggleSubscriptionView(GenericAPIView):
    serializer_class = ToggleSubscriptionSerializer

    def post(self, request, *args, **kwargs):
        """Метод для добавления и удаления подписки на курс"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_id = serializer.validated_data["course_id"]
        user = request.user

        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(owner=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(owner=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})
