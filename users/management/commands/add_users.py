from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создание тестовых пользователей"

    def handle(self, *args, **kwargs):
        # Удаляем существующих пользователей
        User.objects.all().delete()

        # Создаем или обновляем группу модераторов
        moderators_group, created = Group.objects.get_or_create(name="moders")
        if created:
            self.stdout.write(self.style.SUCCESS("Группа moders создана"))

        # Список пользователей для создания
        users_data = [
            # Модератор
            {
                "email": "test1@example.com",
                "is_moder": True,
            },
            # Обычные пользователи
            {
                "email": "test2@example.com",
                "is_moder": False,
            },
            {
                "email": "test3@example.com",
                "is_moder": False,
            },
            {
                "email": "test4@example.com",
                "is_moder": False,
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

            # Добавляем в группу moders
            if user_data.get("is_moder", False):
                user.groups.add(moderators_group)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Пользователь {user.email} добавлен в группу moders"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Все пользователи успешно созданы"))
