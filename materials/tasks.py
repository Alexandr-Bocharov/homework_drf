from celery import shared_task
from django.core.mail import send_mail
from config import settings
from .models import Course, Lesson, Subscription

from users.models import User


@shared_task
def send_message_about_update(course_id, lesson_id):
    """ Отправка сообщений всем пользователям, которые подписаны на рассылку курса, об обновлении материалов """

    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id)

    subscriptions = Subscription.objects.filter(course=course).select_related('owner')
    email_recipients = [sub.owner.email for sub in subscriptions]

    subject = f"Обновление курса!"
    message = f'Обновление в курсе "{course.name}"'

    if email_recipients:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            email_recipients,
        )
