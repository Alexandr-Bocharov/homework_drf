from datetime import datetime
from rest_framework.response import Response

from django.shortcuts import render
from rest_framework import generics

from users.permissions import IsOwner, IsIam
from users.serializers import UserSerializer, PaymentSerializer, UserRetrieveSerializer
from users.models import User, Payment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.services import create_stripe_price, create_stripe_session, create_product, retrieve_stripe_session
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsIam)

    def get_object(self):
        return self.request.user


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated,)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ("payment_date",)
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        if payment.payment_method == "transfer_to_account":
            payment.payment_date = datetime.now().date()

            product = create_product(payment.paid_course.id)
            price = create_stripe_price(payment.payment_amount, product.name)
            session = create_stripe_session(price.get('id'))

            session_id, session_link = session
            payment.session_id = session_id
            payment.link = session_link

            payment.save()


# доп. задание
class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # print(retrieve_stripe_session(instance.session_id).payment_status)
        instance.payment_status = retrieve_stripe_session(instance.session_id).payment_status
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
