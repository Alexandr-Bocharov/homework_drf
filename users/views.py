from django.shortcuts import render
from rest_framework import generics
from users.serializers import (UserSerializer, PaymentSerializer, UserRetrieveSerializer)
from users.models import User, Payment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ("payment_date",)
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
