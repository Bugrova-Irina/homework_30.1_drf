from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription

import logging
logger = logging.getLogger(__name__)

@shared_task
def send_email_about_course_update():
    """
    Отправляет ежедневное сообщение пользователю об обновлениях курсов
    за последние 24 часа
    """
    logger.info("Запуск задачи отправки уведомлений об обновлениях курсов")

    # время 24 часа назад
    time_threshold = timezone.now() - timedelta(hours=24)
    # Получаем все активные подписки
    subscriptions = Subscription.objects.filter(status=True).select_related('user', 'subscribe_course')
    user_updates = {}

    for subscription in subscriptions:
        course = subscription.subscribe_course
        user = subscription.user

        # Проверяем обновление курса за последние 24 часа
        if course.last_update_course >= time_threshold:
            if user.email not in user_updates:
                user_updates[user.email] = []
            user_updates[user.email].append(f"Курс '{course.title}' был обновлен")

        # Проверяем обновление уроков курса за последние 24 часа
        recent_lessons = course.lessons.filter(last_update_lesson__gte=time_threshold)
        if recent_lessons.exists():
            if user.email not in user_updates:
                user_updates[user.email] = []
            user_updates[user.email].append(f"В курсе '{course.title}' обновлены уроки")

    # Отправляем письма пользователям
    for email, updates in user_updates.items():
        if updates:
            message = "За последние 24 часа произошли следующие обновления:\n\n" + "\n".join(updates)
            try:
                send_mail(
                    "Ежедневное обновление курсов",
                    message,
                    EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                logger.info(f"Уведомление отправлено на {email}")
            except Exception as e:
                logger.error(f"Ошибка при отправке письма на {email}: {str(e)}")

    logger.info(f"Задача завершена. Обработано пользователей: {len(user_updates)}")

# Проверка работы отправки писем с помощью тестовой задачи
@shared_task
def test_email():
    send_mail(
        "Тестовое письмо",
        "Это тестовое письмо из Celery",
        EMAIL_HOST_USER,
        ["your-email@example.com"],
        fail_silently=False,
    )
