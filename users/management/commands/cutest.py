from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Создание пользователя test'

    def handle(self, *args, **options):
        user = User.objects.create(
            email='test333@sky.pro',
            first_name='test333',
            last_name='test333',
            is_staff=False,
            is_superuser=False,
        )

        user.set_password('123s')
        user.save()



