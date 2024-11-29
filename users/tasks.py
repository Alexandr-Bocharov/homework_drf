from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_last_login():
    """ Проверка активности пользователя """
    users = User.objects.all()
    for user in users:
        if (timezone.now().date() - user.last_login).days > 30:
            if user.is_active:
                user.is_active = False
                user.save()
                print("пользователь заблокирован")
        else:
            print("пользователь недавно заходил в сеть")