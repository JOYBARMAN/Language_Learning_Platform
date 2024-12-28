from django.contrib import admin

from .models import Quiz, Question, QuizSubmission, LearnerQuizQuestionAnswer


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(QuizSubmission)
admin.site.register(LearnerQuizQuestionAnswer)
