from django.db.models import Count, Subquery, OuterRef, Sum, IntegerField

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import (
    CourseSerializer,
    CourseDetailWithFullInfoSerializer,
    CourseLessonSerializer,
    CourseReviewSerializer,
    CourseEnrollmentSerializer,
)
from .models import (
    Course,
    CourseLessonLecture,
    CourseEnrollment,
    CourseLesson,
    CourseReview,
)

from django_filters.rest_framework import DjangoFilterBackend


class CourseListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "created_at",
        "created_by__uid",
    ]
    search_fields = [
        "title",
        "category__name",
    ]
    filterset_fields = [
        "category__uid",
        "category__name",
    ]

    def get_queryset(self):
        # Subquery to calculate the total duration for each course
        duration_subquery = (
            CourseLessonLecture.objects.filter(course_lesson__course=OuterRef("pk"))
            .values("course_lesson__course")
            .annotate(total_duration=Sum("duration"))
            .values("total_duration")
        )

        return (
            Course.objects.filter()
            .select_related("created_by", "category", "coursedetail")
            .annotate(
                lessons=Count("courselesson"),
                total_duration=Subquery(duration_subquery),
            )
        )


class CourseDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseDetailWithFullInfoSerializer

    def get_object(self):
        course_uid = self.kwargs.get("uid")
        try:
            total_lectures_subquery = (
                CourseLessonLecture.objects.filter(course_lesson__course=OuterRef("pk"))
                .values("course_lesson__course")
                .annotate(total_lectures=Count("pk"))
                .values("total_lectures")
            )
            total_enrollments_subquery = (
                CourseEnrollment.objects.filter(course=OuterRef("pk"))
                .values("course")
                .annotate(total_enrollments=Count("pk"))
                .values("total_enrollments")
            )

            return (
                Course.objects.select_related("created_by", "category", "coursedetail")
                .annotate(
                    lessons=Count("courselesson"),
                    total_duration=Subquery(
                        CourseLessonLecture.objects.filter(
                            course_lesson__course=OuterRef("pk")
                        )
                        .values("course_lesson__course")
                        .annotate(total_duration=Sum("duration"))
                        .values("total_duration"),
                    ),
                    total_lectures=Subquery(
                        total_lectures_subquery, output_field=IntegerField()
                    ),
                    total_enrollment=Subquery(
                        total_enrollments_subquery, output_field=IntegerField()
                    ),
                )
                .get(uid=course_uid)
            )
        except Course.DoesNotExist:
            raise NotFound("Course with this uid not found")


class CourseCurriculumView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseLessonSerializer

    def get_queryset(self):
        course_uid = self.kwargs.get("uid")
        return CourseLesson.objects.filter(course__uid=course_uid).prefetch_related(
            "courselessonlecture_set",
            "quiz_set",
        )


class CourseReviewView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseReviewSerializer

    def get_queryset(self):
        course_uid = self.kwargs.get("uid")
        return CourseReview.objects.filter(course__uid=course_uid).select_related(
            "user"
        )


class CourseEnrollmentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseEnrollmentSerializer