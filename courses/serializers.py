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

from quizzes.serializers import QuizMinSerializer

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
            "image_url",
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


class CourseLessonLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLessonLecture
        fields = [
            "uid",
            "title",
            "description",
            "video_url",
            "duration",
            "created_at",
        ]


class CourseLessonSerializer(serializers.ModelSerializer):
    courselessonlecture_set = CourseLessonLectureSerializer(read_only=True, many=True)
    quiz_set = QuizMinSerializer(many=True, read_only=True)

    class Meta:
        model = CourseLesson
        fields = [
            "uid",
            "title",
            "description",
            "video_url",
            "created_at",
            "courselessonlecture_set",
            "quiz_set",
        ]


class CourseReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CourseReview
        fields = [
            "uid",
            "user",
            "rating",
            "review",
            "created_at",
        ]


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = [
            "uid",
            "course",
            "user",
            "enrolled_at",
            "payment_status",
            "created_at",
        ]
        read_only_fields = fields

    def create(self, validated_data):
        course_uid = self.context["view"].kwargs.get("uid")
        user = self.context["request"].user
        # Get course object
        course = Course.objects.filter(uid=course_uid).first()
        if not course:
            raise serializers.ValidationError("Course not found")
        # Enroll user on the course
        enrollment, created = CourseEnrollment.objects.get_or_create(
            user=user, course=course
        )

        return enrollment


class CourseMinSerializer(serializers.ModelSerializer):
    coursedetail = CourseDetailSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ["uid", "title", "coursedetail"]


class CourseContinueSerializer(serializers.ModelSerializer):
    course = CourseMinSerializer(read_only=True)
    courselessonlecture_set = CourseLessonLectureSerializer(read_only=True, many=True)
    is_quiz_completed = serializers.BooleanField(default=False)

    class Meta:
        model = CourseLesson
        fields = [
            "uid",
            "title",
            "description",
            "video_url",
            "created_at",
            "course",
            "courselessonlecture_set",
            "is_quiz_completed",
        ]


class LectureCompleteSerializer(serializers.Serializer):
    is_completed = serializers.BooleanField(default=True)

    def create(self, validated_data):
        user = self.context["request"].user
        lecture_uid = self.context["view"].kwargs.get("lecture_uid")
        lesson_lecture = CourseLessonLecture.objects.filter(uid=lecture_uid).first()
        if not lesson_lecture:
            raise serializers.ValidationError("Lecture not found")

        course_enrollment = CourseEnrollment.objects.filter(
            user=user, course=lesson_lecture.course_lesson.course
        ).first()
        if not course_enrollment:
            raise serializers.ValidationError("You are not enrolled in this course")

        course_enrollment.completed_lecture.add(lesson_lecture)

        return {}
