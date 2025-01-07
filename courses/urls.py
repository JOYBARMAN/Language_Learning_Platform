from django.urls import path

from .views import (
    CourseListView,
    CourseDetailView,
    CourseCurriculumView,
    CourseReviewView,
    CourseEnrollmentView,
    CourseContinueLearningView,
    CourseLessonLectureCompleteView,
)
from quizzes.views import (
    LessonQuizView,
    LearnerQuizSubmission,
    QuizSubmissionResultView,
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
    path(
        "/<str:uid>/enrollment",
        CourseEnrollmentView.as_view(),
        name="course-enrollment",
    ),
    path(
        "/<str:uid>/continue",
        CourseContinueLearningView.as_view(),
        name="course-continue",
    ),
    path(
        "/<str:course_uid>/lesson/<str:lesson_uid>/quiz",
        LessonQuizView.as_view(),
        name="lesson-quiz",
    ),
    path(
        "/<str:uid>/lecture/<str:lecture_uid>/lecture-complete",
        CourseLessonLectureCompleteView.as_view(),
        name="lesson-lecture-complete",
    ),
    path(
        "/<str:course_uid>/lesson/<str:lesson_uid>/quiz-submission",
        LearnerQuizSubmission.as_view(),
        name="lesson-quiz-submission",
    ),
    path(
        "/<str:course_uid>/lesson/<str:lesson_uid>/quiz-submission-result",
        QuizSubmissionResultView.as_view(),
        name="lesson-quiz-submission-result",
    ),
]
