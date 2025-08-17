from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Создание тестовых платежей"

    def handle(self, *args, **kwargs):
        # Удаляем существующие платежи
        Payment.objects.all().delete()

        # Список платежей для добавления в БД
        payments_data = [
            {
                "user_id": 1,
                "payment_date": "2025-05-01 00:00:00",
                "paid_course_id": 1,
                "amount": 10000,
                "payment_type": "transfer",
            },
            {
                "user_id": 2,
                "payment_date": "2025-05-02 00:00:00",
                "paid_course_id": 2,
                "amount": 12000,
                "payment_type": "cash",
            },
            {
                "user_id": 3,
                "payment_date": "2025-05-03 00:00:00",
                "paid_lesson_id": 2,
                "amount": 1000,
                "payment_type": "transfer",
            },
            {
                "user_id": 4,
                "payment_date": "2025-05-04 00:00:00",
                "paid_lesson_id": 1,
                "amount": 800,
                "payment_type": "cash",
            }
        ]

        # Создаем оплату
        for payment_data in payments_data:
            # Получаем объекты по id
            try:
                user = User.objects.get(id=payment_data["user_id"])

                paid_course = None
                if "paid_course_id" in payment_data:
                    paid_course = Course.objects.get(id=payment_data["paid_course_id"])

                paid_lesson = None
                if "paid_lesson_id" in payment_data:
                    paid_lesson = Lesson.objects.get(id=payment_data["paid_lesson_id"])

                payment = Payment.objects.create(
                    user=user,
                    payment_date=payment_data["payment_date"],
                    paid_course=paid_course,
                    paid_lesson=paid_lesson,
                    amount=payment_data["amount"],
                    payment_type=payment_data["payment_type"],
                )

                self.stdout.write(
                    self.style.SUCCESS(f"Создана оплата для пользователя: {user.email}")
                )

            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Пользователь с ID {payment_data['user_id']} не найден")
                )
            except Course.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Курс с ID {payment_data.get('paid_course_id')} не найден")
                )
            except Lesson.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Урок с ID {payment_data.get('paid_lesson_id')} не найден")
                )

        self.stdout.write(self.style.SUCCESS("Все оплаты успешно созданы"))
