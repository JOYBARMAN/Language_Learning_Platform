from rest_framework import serializers

from .models import Quiz, Question, QuizSubmission, LearnerQuizQuestionAnswer

from core.serializers import UserSerializer
from .choices import QuizSubmissionStatusChoices


class QuizMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            "uid",
            "title",
            "description",
            "duration",
            "total_marks",
            "created_at",
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "uid",
            "question",
            "marks",
            "options",
            "time",
            "created_at",
        ]


class QuizQuestionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Quiz
        fields = [
            "uid",
            "title",
            "description",
            "duration",
            "total_marks",
            "questions",
            "created_at",
        ]


class QuizAnswerSubmission(serializers.Serializer):
    answer = serializers.ListField(write_only=True)
    question_uid = serializers.UUIDField(write_only=True)

    def create(self, validated_data):
        user = self.context["request"].user
        lesson_uid = self.context["view"].kwargs.get("lesson_uid")

        question = Question.objects.filter(uid=validated_data["question_uid"]).first()
        if not question:
            raise serializers.ValidationError("Question not found")

        quiz_submission, created = QuizSubmission.objects.get_or_create(
            learner=user, quiz=question.quiz
        )
        is_correct_answer = sorted(validated_data["answer"]) == sorted(question.answer)

        if is_correct_answer:
            quiz_submission.total_marks += question.marks

        quiz_submission.status = QuizSubmissionStatusChoices.SUBMITTED
        quiz_submission.save()

        learner_quiz_question_answer, created = (
            LearnerQuizQuestionAnswer.objects.get_or_create(
                question=question, quiz_submission=quiz_submission
            )
        )
        learner_quiz_question_answer.answer = validated_data["answer"]
        learner_quiz_question_answer.is_correct = is_correct_answer
        learner_quiz_question_answer.save()

        return {}


class QuizQuestionWithAnswerSerializer(QuestionSerializer):
    class Meta(QuestionSerializer.Meta):
        fields = QuestionSerializer.Meta.fields + ["answer"]


class QuizWithAnswerSerializer(serializers.ModelSerializer):
    questions = QuizQuestionWithAnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Quiz
        fields = [
            "uid",
            "title",
            "description",
            "duration",
            "total_marks",
            "questions",
            "created_at",
        ]


class UserAnswerSerializer(serializers.ModelSerializer):
    question = QuizQuestionWithAnswerSerializer(read_only=True)

    class Meta:
        model = LearnerQuizQuestionAnswer
        fields = [
            "question",
            "answer",
            "is_correct",
        ]


class QuizSubmissionResultSerializer(serializers.ModelSerializer):
    quiz = QuizWithAnswerSerializer(read_only=True)
    learner = UserSerializer(read_only=True)
    learnerquizquestionanswer_set = UserAnswerSerializer(read_only=True, many=True)
    class Meta:
        model = QuizSubmission
        fields = [
            "uid",
            "quiz",
            "status",
            "total_marks",
            "submitted_at",
            "learner",
            "learnerquizquestionanswer_set",
            "created_at",
        ]