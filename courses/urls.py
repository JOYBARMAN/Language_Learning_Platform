from django.urls import path

from .views import (
    CourseListView,
    CourseDetailView,
    CourseCurriculumView,
    CourseReviewView,
    CourseEnrollmentView,
)

urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path("/<str:uid>", CourseDetailView.as_view(), name="course-detail"),
    path(
        "/<str:uid>/curriculum",
        CourseCurriculumView.as_view(),
        name="course-curriculum",
    ),
    path("/<str:uid>/reviews", CourseReviewView.as_view(), name="course-review"),
    path("/<str:uid>/enrollment", CourseEnrollmentView.as_view(), name="course-enrollment"),
]
