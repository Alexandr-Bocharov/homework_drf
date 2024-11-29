from rest_framework import serializers

from materials.models import Subscription
from users.models import User, Payment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    subscriptions = serializers.SerializerMethodField()

    def get_subscriptions(self, user):
        return [str(sub.course) for sub in Subscription.objects.filter(owner=user)]

    class Meta:
        model = User
        # fields = ('id', 'email', 'phone', 'city', 'avatar')
        fields = "__all__"


class UserRetrieveSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source="payment_set", many=True)

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar", "payments")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Обновляем поле last_login у пользователя
        self.user.last_login = timezone.now().date()
        self.user.save(update_fields=["last_login"])
        return data
