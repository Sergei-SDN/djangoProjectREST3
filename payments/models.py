from django.db import models

from djangoProjectREST2 import settings
from users.models import User
from application.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}

PAY_CARD = 'card'
PAY_CASH = 'cash'

PAY_TYPES = (
    (PAY_CASH, 'наличные'),
    (PAY_CARD, 'перевод')
)


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь',
                             on_delete=models.SET_NULL, **NULLABLE, related_name='payment')
    pay_date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    payment_type = models.CharField(choices=PAY_TYPES, default=PAY_CASH, max_length=10, verbose_name='способ оплаты')
    is_successful = models.BooleanField(default=False, verbose_name='Статус платежа')
    session = models.CharField(max_length=150, verbose_name='cессия для оплаты', **NULLABLE)

    def __str__(self):
        return f'{self.user} - {self.pay_date}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'
