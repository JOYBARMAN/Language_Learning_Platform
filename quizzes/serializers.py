from rest_framework import serializers

from .models import Quiz


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
