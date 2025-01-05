from django.urls import path

from .views import CourseListView, CourseDetailView, CourseCurriculumView

urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path("/<str:uid>", CourseDetailView.as_view(), name="course-detail"),
    path("/<str:uid>/curriculum", CourseCurriculumView.as_view(), name="course-curriculum"),
]
