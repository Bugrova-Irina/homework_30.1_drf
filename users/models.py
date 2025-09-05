from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    username = None  # Авторизация по email

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )

    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    # Авторизация по email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]


class Payment(models.Model):
    """Модель платежей"""

    # Вид оплаты
    TRANSFER = "transfer"
    CASH = "cash"
    PAYMENT_CHOICES = [
        (TRANSFER, "Оплата по счету"),
        (CASH, "Оплата наличными"),
    ]

    user = models.ForeignKey(
        "User",  # Строковая ссылка на модель User
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    payment_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата оплаты", help_text="Укажите дату оплаты"
    )
    paid_course = models.ForeignKey(
        "materials.Course",  # Строковая ссылка на модель из другого приложения
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Оплаченный курс",
        help_text="Введите название курса",
    )
    paid_lesson = models.ForeignKey(
        "materials.Lesson",  # Строковая ссылка на модель из другого приложения
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Оплаченный урок",
        help_text="Введите название урока",
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        verbose_name="Сумма оплаты",
        help_text="Введите сумму оплаты",
    )
    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default=TRANSFER,
        verbose_name="Вид оплаты",
        help_text="Укажите вид оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии",
        help_text="Укажите ID сессии",
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Платеж от {self.user} на сумму {self.amount}."
