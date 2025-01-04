from django.db import models

from core.models import User

from shared.base_model import BaseModel

from courses.models import Course, CourseLesson

from quizzes.choices import QuizSubmissionStatusChoices


class Quiz(BaseModel):
    # Relationship
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(CourseLesson, on_delete=models.CASCADE, null=True, blank=True)
    # General Fields
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    total_marks = models.PositiveIntegerField(default=0)
    questions = models.ManyToManyField("Question", related_name="quizzes", blank=True)

    def __str__(self):
        return self.title


class Question(BaseModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    marks = models.PositiveIntegerField(default=1)
    options = models.JSONField(default=dict, blank=True, null=True)
    answer = models.JSONField(default=list, blank=True, null=True)
    time = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if self.pk:
            # Fetch the existing marks value from the database
            old_marks = (
                self.__class__.objects.filter(pk=self.pk)
                .values_list("marks", flat=True)
                .first()
            )
            if old_marks is not None:
                # Update total_marks by subtracting old marks and adding new marks
                self.quiz.total_marks += self.marks - old_marks
                self.quiz.save()
        else:
            # If creating a new instance, add marks to total_marks
            self.quiz.total_marks += self.marks
            self.quiz.save()

        super().save(*args, **kwargs)

        # Add the question to the quiz
        self.quiz.questions.add(self)


class QuizSubmission(BaseModel):
    # Relationship
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    # General Fields
    status = models.CharField(max_length=20, choices=QuizSubmissionStatusChoices.choices, default=QuizSubmissionStatusChoices.PENDING)
    total_marks = models.PositiveIntegerField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.quiz.title} - {self.learner.email}"


class LearnerQuizQuestionAnswer(BaseModel):
    quiz_submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.JSONField(default=list, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    time_taken = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.question.question} - {self.quiz_submission.learner.email}"
