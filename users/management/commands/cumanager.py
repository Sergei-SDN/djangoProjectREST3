from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Создание пользователя manager'

    def handle(self, *args, **options):
        user = User.objects.create(
            email='moderator1@sky.pro',
            first_name='moderator1',
            last_name='moderator1',
            is_staff=True,
            is_superuser=False,
            role='moderator'
        )

        user.set_password('123s')
        user.save()



