from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Создание пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # Доступно неавторизованным пользователям

    def perform_create(self, serializer):
        """Получение пользователя"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)  # Хеширование пароля
        user.save()


class PaymentViewSet(ModelViewSet):
    """CRUD для платежей"""
    queryset = Payment.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_type",
    )
    ordering_fields = ("payment_date",)

    def get_serializer_class(self):
        return PaymentSerializer
