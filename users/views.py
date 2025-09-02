from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Subscription
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import convert_rub_to_usd, create_stripe_price, create_stripe_session, create_stripe_product


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


class SubscriptionAPIView(APIView):
    """Создание подписки на курс"""

    def post(self, *args, **kwargs):
        # управление подпиской
        user = self.request.user
        course_id = self.request.data.get("subscribe_course")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item, created = Subscription.objects.get_or_create(
            user=user, subscribe_course=course_item
        )

        if created:
            message = "Подписка на обновление курса добавлена"
        else:
            subs_item.delete()
            message = "Подписка на обновление курса удалена"
        return Response({"message": message})


class PaymentCreateAPIView(CreateAPIView):
    """ Класс создания ссылки на оплату """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_usd = convert_rub_to_usd(payment.amount)
        product = create_stripe_product(
            name=f"Payment for {
            payment.paid_course or payment.paid_lesson
            }"
        )
        price = create_stripe_price(amount_in_usd, product)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
