from rest_framework import serializers

from core.serializers import UserSerializer

from .models import (
    Course,
    CourseLesson,
    CourseLessonLecture,
    CourseReview,
    ListTypeDescription,
    CourseDetail,
    CourseEnrollment,
)
from .choices import DescriptionTypeChoices

from categories.serializers import CategorySerializer


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetail
        fields = [
            "uid",
            "description",
            "price",
            "discount",
            "actual_price",
            "language",
            "skill_level",
            "deadline",
            "certificate",
        ]


class ListTypeDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListTypeDescription
        fields = [
            "uid",
            "text",
            "description",
            "type",
            "created_at",
        ]


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    coursedetail = CourseDetailSerializer(read_only=True)
    lessons = serializers.IntegerField(default=None)
    total_duration = serializers.DurationField(default=None)

    class Meta:
        model = Course
        fields = [
            "uid",
            "title",
            "image",
            "video_url",
            "rating",
            "lessons",
            "total_duration",
            "category",
            "created_by",
            "coursedetail",
            "created_at",
        ]


class CourseDetailWithFullInfoSerializer(CourseSerializer):
    what_you_will_learn = serializers.SerializerMethodField()
    requirements = serializers.SerializerMethodField()
    total_lectures = serializers.IntegerField(default=None)
    total_enrollment = serializers.IntegerField(default=None)

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + [
            "what_you_will_learn",
            "requirements",
            "total_lectures",
            "total_enrollment",
        ]
        read_only_fields = fields

    def get_what_you_will_learn(self, obj):
        return ListTypeDescriptionSerializer(
            ListTypeDescription.objects.filter(
                course=obj, type=DescriptionTypeChoices.LEARNING_OUTCOMES
            ),
            many=True,
        ).data

    def get_requirements(self, obj):
        return ListTypeDescriptionSerializer(
            ListTypeDescription.objects.filter(
                course=obj, type=DescriptionTypeChoices.REQUIREMENTS
            ),
            many=True,
        ).data
