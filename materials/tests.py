from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    """Тестирование CRUD уроков"""

    def setUp(self):
        # Экземпляр пользователя
        self.user = User.objects.create(email="admin@example.com")
        # Экземпляр курса
        self.course = Course.objects.create(
            title="Python",
            description="Programming language",
            owner=self.user,
        )
        # Экземпляр урока
        self.lesson = Lesson.objects.create(
            title="Lesson 1",
            description="The beginning",
            video="https://youtube.com/",
            course=self.course,
            owner=self.user,
        )
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        # Проверяем вывод информации об уроке
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        # Проверяем создание урока
        url = reverse("materials:lessons_create")
        data = {"title": "Lesson 2", "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        # Проверяем обновление информации об уроке
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"title": "Lesson 3"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Lesson 3")

    def test_lesson_delete(self):
        # Проверяем удаление урока
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        # Проверяем вывод списка уроков
        url = reverse("materials:lessons-list")
        response = self.client.get(url)
        data = response.json()
        # result = {
        #     "count": 1,
        #     "next": None,
        #     "previous": None,
        #     "results": [
        #         {
        #             "id": self.lesson.pk,
        #             "video": "https://youtube.com/",
        #             "title": self.lesson.title,
        #             "preview": None,
        #             "description": self.lesson.description,
        #             "course": self.course.pk,
        #             "owner": self.user.pk,
        #         }
        #     ],
        # }

        # Проверяем статус код
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем основную структуру ответа
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)
        self.assertEqual(len(data["results"]), 1)

        # Проверяем данные первого урока
        lesson_data = data["result"][0]
        self.assertEqual(lesson_data["id"], self.lesson.pk)
        self.assertEqual(lesson_data["video"], "https://youtube.com")
        self.assertEqual(lesson_data["title"], self.lesson.title)
        self.assertEqual(lesson_data["preview"], None)
        self.assertEqual(lesson_data["description"], self.lesson.description)
        self.assertEqual(lesson_data["course"], self.course.pk)
        self.assertEqual(lesson_data["owner"], self.user.pk)

        # Проверяем, что полу last_update_lesson присутствует,
        # но не проверяем точное значение
        self.assertEqual("last_update_lesson", lesson_data)


class SubscriptionTestCase(APITestCase):
    """Тестирование работы подписки"""

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(title="Python", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        url = reverse("materials:subscription")
        data = {"subscribe_course": self.course.id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["message"], "Подписка на обновление курса добавлена"
        )
