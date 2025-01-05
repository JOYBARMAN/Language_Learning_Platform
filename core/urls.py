from django.urls import path, include

from .views import MeInfo

urlpatterns = [
    path("", MeInfo.as_view(), name="me-info"),
]
