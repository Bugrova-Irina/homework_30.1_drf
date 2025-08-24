from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer)
from users.permissions import IsModer


class CourseViewSet(ModelViewSet):
    """CRUD курсов"""

    queryset = Course.objects.all()

    def get_serializer_class(self):
        # если нужно посмотреть детальную информацию о курсе
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        """
        Назначение прав модераторам
        """
        # Модератор не может создавать
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        # Модератор может обновлять и просматривать
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer,)
        # Модератор не может удалять
        elif self.action == 'destroy':
            self.permission_classes = (~IsModer,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    """Создание урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer)


class LessonListApiView(ListAPIView):
    """Вывод списка уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveApiView(RetrieveAPIView):
    """Вывод страницы урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer)


class LessonUpdateApiView(UpdateAPIView):
    """Обновление урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer)


class LessonDestroyApiView(DestroyAPIView):
    """Удаление урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer)
