from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from courses.models import CourseEnrollment, CourseLesson

from quizzes.models import Quiz, QuizSubmission
from quizzes.serializers import (
    QuizQuestionSerializer,
    QuizAnswerSubmission,
    QuizSubmissionResultSerializer,
)


class LessonQuizView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizQuestionSerializer

    def get_queryset(self):
        course_uid = self.kwargs.get("course_uid")
        lesson_uid = self.kwargs.get("lesson_uid")

        course_enrollment = CourseEnrollment.objects.filter(
            user=self.request.user, course__uid=course_uid
        ).first()
        if not course_enrollment:
            raise NotFound("You are not enrolled in this course")

        course_lesson = CourseLesson.objects.filter(
            course__uid=course_uid, uid=lesson_uid
        ).first()
        if not course_lesson:
            raise NotFound("Lesson not found")

        course_lesson_lecture = course_lesson.courselessonlecture_set
        for lecture in course_lesson_lecture.all():
            if not lecture in course_enrollment.completed_lecture.all():
                raise NotFound("You have not completed the previous lectures")

        return Quiz.objects.filter(lesson=course_lesson).prefetch_related("questions")


class LearnerQuizSubmission(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizAnswerSubmission


class QuizSubmissionResultView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSubmissionResultSerializer

    def get_queryset(self):
        user = self.request.user
        lesson_uid = self.kwargs.get("lesson_uid")

        return [
            QuizSubmission.objects.filter(learner=user, quiz__lesson__uid=lesson_uid)
            .select_related("quiz", "learner")
            .prefetch_related("learnerquizquestionanswer_set")
            .first()
        ]
