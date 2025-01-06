from django.urls import path, include

from .views import MeInfo, MeCoursesView

urlpatterns = [
    path("", MeInfo.as_view(), name="me-info"),
    path("/courses",MeCoursesView.as_view(), name="me-courses"),
]
