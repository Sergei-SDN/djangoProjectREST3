from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Создание Админа'

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='admin',
            last_name='sky',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('123s')
        user.save()
