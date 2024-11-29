from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import LinkValidator
from users.serializers import UserSerializer


class LessonSerializer(serializers.ModelSerializer):
    # link = serializers.CharField(validators=[validate_url])
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkValidator(field="link")]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    is_sub = serializers.SerializerMethodField()
    # lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)
    # sub_users = serializers.SerializerMethodField()

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_sub(self, course):
        cur_user = self.context["request"].user
        return Subscription.objects.filter(course=course, owner=cur_user).exists()

    # def get_sub_users(self, course):
    #     user_serializer = UserSerializer
    #     return [course for course in Course.objects.all() if course.name in user_serializer.subscriptions]

    # def get_lessons(self, course):
    #     return [{"name": lesson.name, "description": lesson.description}
    #             for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        # fields = (
        #     "id",
        #     "name",
        #     "description",
        #     "lessons_count",
        #     "lessons",
        #     "owner",
        #     "is_sub",
        #     "updated_at",
        # )
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"


class ToggleSubscriptionSerializer(serializers.Serializer):

    course_id = serializers.IntegerField()

    def validate_course_id(self, value):
        if not Course.objects.filter(id=value).exists():
            raise serializers.ValidationError("Курс с указанным ID не найден.")
        return value
