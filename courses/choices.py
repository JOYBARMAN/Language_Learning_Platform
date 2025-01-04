from django.db import models


class SkillLevelChoices(models.TextChoices):
    BEGINNER = "BEGINNER", "Beginner"
    INTERMEDIATE = "INTERMEDIATE", "Intermediate"
    ADVANCED = "ADVANCED", "Advanced"
    EXPERT = "EXPERT", "Expert"
    ALL = "ALL", "All"


class CertificateChoices(models.TextChoices):
    YES = "YES", "Yes"
    NO = "NO", "No"


class DescriptionTypeChoices(models.TextChoices):
    REQUIREMENTS = "REQUIREMENTS", "Requirements"
    LEARNING_OUTCOMES = "LEARNING_OUTCOMES", "Learning Outcomes"
    UNDEFINED = "UNDEFINED", "Undefined"


class CourseEnrollmentPaymentStatusChoices(models.TextChoices):
    PENDING = "PENDING", "Pending"
    COMPLETED = "COMPLETED", "Completed"
    REFUNDED = "REFUNDED", "Refunded"
    CANCELLED = "CANCELLED", "Cancelled"
