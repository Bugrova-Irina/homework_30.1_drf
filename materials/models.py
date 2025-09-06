from django.db import models


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(
        max_length=200,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/images",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Укажите описание курса",
    )
    owner = models.ForeignKey(
        "users.User",  # Строковая ссылка на модель User
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )
    last_update_course = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего обновления курса",
        help_text="Укажите дату последнего обновления курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(
        max_length=200,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    preview = models.ImageField(
        upload_to="materials/images",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Укажите описание урока",
    )
    video = models.CharField(
        max_length=350,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео-урок",
        help_text="Укажите ссылку на видео-урок",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Укажите курс",
        related_name="lessons",
    )
    owner = models.ForeignKey(
        "users.User",  # Строковая ссылка на модель User
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
    )
    last_update_lesson = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего обновления курса",
        help_text="Укажите дату последнего обновления курса",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """Модель подписки"""

    user = models.ForeignKey(
        "users.User",  # Строковая ссылка на модель User
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    subscribe_course = models.ForeignKey(
        "materials.Course",  # Строковая ссылка на модель из другого приложения
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Курс, на который подписан пользователь",
        help_text="Введите название курса",
    )
    status = models.BooleanField(
        default=True,
        blank=True,
        null=True,
        verbose_name="Статус подписки",
        help_text="Укажите статус подписки",
    )

    def __str__(self):
        return f"{self.user} подписан на {self.subscribe_course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
