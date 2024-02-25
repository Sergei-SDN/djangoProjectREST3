from rest_framework import serializers
from payments.serializers import PaymentSerializer
from .models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя с историей платежей."""
    payments = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'avatar', 'country', 'payments']


class UserProfilePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'last_name']
