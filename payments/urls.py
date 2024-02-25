from django.urls import path

from .apps import PaymentsConfig
from .views import PaymentListAPIView, PaymentCreateAPIView, PaymentRetrieveAPIView

app_name = PaymentsConfig.name

urlpatterns = [
    path('api/payment/', PaymentListAPIView.as_view(), name='payment-list'),
    path('api/payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('api/payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment-detail'),
]
