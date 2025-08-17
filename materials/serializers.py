from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(ModelSerializer):
    count_lessons_into_the_course = SerializerMethodField()

    # Подсчет уроков в курсе
    def get_count_lessons_into_the_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ('title', 'preview', 'description', 'count_lessons_into_the_course',)


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
