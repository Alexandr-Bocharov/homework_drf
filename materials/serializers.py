from rest_framework import serializers
from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    # lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    # def get_lessons(self, course):
    #     return [{"name": lesson.name, "description": lesson.description}
    #             for lesson in Lesson.objects.filter(course=course)]



    class Meta:
        model = Course
        fields = ("id", "name", "description", "lessons_count", "lessons")
