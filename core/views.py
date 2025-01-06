from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer

from courses.models import CourseEnrollment
from courses.serializers import CourseEnrollmentSerializer


class MeInfo(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        try:
            return self.request.user
        except User.DoesNotExist:
            raise Http404


class MeCoursesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseEnrollmentSerializer

    def get_queryset(self):
        user = self.request.user
        return CourseEnrollment.objects.filter(user=user).select_related(
            "course__coursedetail",
            "course__created_by",
            "course__category",
            "user",
        )
