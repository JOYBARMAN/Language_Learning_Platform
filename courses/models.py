from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from core.models import User

from categories.models import Category

from shared.base_model import BaseModel

from courses.choices import (
    SkillLevelChoices,
    CertificateChoices,
    DescriptionTypeChoices,
    CourseEnrollmentPaymentStatusChoices,
)


class Course(BaseModel):
    # Relationship Important
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # General Fields
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to="images/course", blank=True, null=True)
    image_url = models.URLField(max_length=1000,null=True, blank=True)
    video_url = models.URLField(max_length=1000, blank=True, null=True)
    rating = models.FloatField(
        default=0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title


class CourseDetail(BaseModel):
    # Relationship
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    # Fields
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    actual_price = models.FloatField(default=0)
    language = models.CharField(max_length=100, null=True, blank=True)
    skill_level = models.CharField(
        max_length=100, choices=SkillLevelChoices.choices, default=SkillLevelChoices.ALL
    )
    deadline = models.DateField(blank=True, null=True)
    certificate = models.CharField(
        max_length=100,
        choices=CertificateChoices.choices,
        default=CertificateChoices.YES,
    )

    class Meta:
        verbose_name = "Course Detail"
        verbose_name_plural = "Course Details"

    def __str__(self):
        return self.course.title

    def save(self, *args, **kwargs):
        self.actual_price = self.price - (self.price * self.discount / 100)
        super(CourseDetail, self).save(*args, **kwargs)


class ListTypeDescription(BaseModel):
    # Relationship
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Fields
    text = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(
        max_length=100,
        choices=DescriptionTypeChoices.choices,
        default=DescriptionTypeChoices.UNDEFINED,
    )

    class Meta:
        verbose_name = "List Type Description"
        verbose_name_plural = "List Type Descriptions"

    def __str__(self):
        return self.text


class CourseLesson(BaseModel):
    # Relationship
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # General Fields
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(max_length=1000, blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)

    class Meta:
        verbose_name = "Course Lesson"
        verbose_name_plural = "Course Lessons"

    def __str__(self):
        return self.title


class CourseLessonLecture(BaseModel):
    # Relationship
    course_lesson = models.ForeignKey(CourseLesson, on_delete=models.CASCADE)
    # General Fields
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(max_length=1000, blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)

    class Meta:
        verbose_name = "Course Lesson Lecture"
        verbose_name_plural = "Course Lesson Lectures"

    def __str__(self):
        return self.title


class CourseReview(BaseModel):
    # Relationship
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # General Fields
    rating = models.FloatField(
        default=0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    review = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Course Review"
        verbose_name_plural = "Course Reviews"

    def __str__(self):
        return self.course.title


class CourseEnrollment(BaseModel):
    # Relationship
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_lecture = models.ManyToManyField(CourseLessonLecture, blank=True)
    # General Fields
    payment_status = models.CharField(
        max_length=100,
        choices=CourseEnrollmentPaymentStatusChoices.choices,
        default=CourseEnrollmentPaymentStatusChoices.PENDING,
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Course Enrollment"
        verbose_name_plural = "Course Enrollments"
        constraints = [
            models.UniqueConstraint(
                fields=["course", "user"], name="unique_course_enrollment"
            )
        ]

    def __str__(self):
        return self.course.title
