from django.shortcuts import render
from rest_framework import viewsets, generics
from materials.serializers import CourseSerializer, LessonSerializer
from materials.models import Course, Lesson
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

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
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()




class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~IsModer)

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | IsModer)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | IsModer)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~IsModer | IsOwner)
