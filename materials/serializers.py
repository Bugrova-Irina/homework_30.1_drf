from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import YoutubeURLValidator


class LessonSerializer(serializers.ModelSerializer):
    # Явно определяем поле video с валидатором
    video = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        validators=[YoutubeURLValidator()],
        max_length=350,
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    # Вывод информации об уроке
    lesson_info = LessonSerializer(many=True, source="lessons", read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lessons_into_the_course = SerializerMethodField()
    subscription = SerializerMethodField()
    # Вывод информации об уроке
    lesson_info = LessonSerializer(many=True, source="lessons", read_only=True)

    # Подсчет уроков в курсе
    def get_count_lessons_into_the_course(self, course):
        return course.lessons.count()

    # Вывод информации о подписке
    def get_subscription(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, subscribe_course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = (
            "title",
            "preview",
            "description",
            "lesson_info",  # вывод информации об уроке
            "count_lessons_into_the_course",  # вывод количества уроков в курсе
            "subscription", # вывод информации о подписке
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Вывод информации о подписке """

    class Meta:
        model = Subscription
        fields = "__all__"
