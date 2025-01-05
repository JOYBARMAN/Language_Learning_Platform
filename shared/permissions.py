from rest_framework.permissions import BasePermission, IsAuthenticated

from core.choices import UserTypeChoices

class IsLearner(BasePermission):
    message = "You must be a learner to access this."

    def has_permission(self, request, view):
        return request.user.user_type == UserTypeChoices.LEARNER

class IsTeacher(BasePermission):
    message = "You must be a teacher to access this."

    def has_permission(self, request, view):
        return request.user.user_type == UserTypeChoices.TEACHER