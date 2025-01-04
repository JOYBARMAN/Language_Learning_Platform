from django.contrib import admin

from .models import (
    Course,
    CourseDetail,
    ListTypeDescription,
    CourseLesson,
    CourseLessonLecture,
    CourseEnrollment,
    CourseReview,
)

admin.site.register(Course)
admin.site.register(CourseDetail)
admin.site.register(ListTypeDescription)
admin.site.register(CourseLesson)
admin.site.register(CourseLessonLecture)
admin.site.register(CourseEnrollment)
admin.site.register(CourseReview)
