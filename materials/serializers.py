from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    # Вывод информации об уроке
    lesson_info = LessonSerializer(many=True, source="lessons", read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
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
