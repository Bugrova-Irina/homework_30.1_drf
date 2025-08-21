from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создание тестовых пользователей"

    def handle(self, *args, **kwargs):
        # Удаляем существующих пользователей
        User.objects.all().delete()

        # Список пользователей для создания
        users_data = [
            {
                "email": "test1@example.com",
            },
            {
                "email": "test2@example.com",
            },
            {
                "email": "test3@example.com",
            },
            {
                "email": "test4@example.com",
            },
        ]

        # Создаем пользователей
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "is_superuser": user_data.get("is_superuser", False),
                    "is_staff": user_data.get("is_staff", False),
                    "is_active": True,
                },
            )

            # Устанавливаем пароль
            if created:
                user.set_password("12345")
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Создан пользователь: {user.email}")
                )

        self.stdout.write(self.style.SUCCESS("Все пользователи успешно созданы"))
