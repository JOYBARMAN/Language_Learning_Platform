from django.db import models


class QuizSubmissionStatusChoices(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUBMITTED = "SUBMITTED", "Submitted"
    GRADED = "GRADED", "Graded"
    CANCELLED = "CANCELLED", "Cancelled"
