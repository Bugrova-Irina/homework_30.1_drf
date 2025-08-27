from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
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
    # Вывод информации об уроке
    lesson_info = LessonSerializer(many=True, source="lessons", read_only=True)

    # Подсчет уроков в курсе
    def get_count_lessons_into_the_course(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = (
            "title",
            "preview",
            "description",
            "lesson_info",  # вывод информации об уроке
            "count_lessons_into_the_course",  # вывод количества уроков в курсе
        )
