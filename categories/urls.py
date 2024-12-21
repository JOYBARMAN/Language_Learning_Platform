from django.urls import path

from categories.views import CategoryView, CategoryDetailView

urlpatterns = [
    path("", CategoryView.as_view(), name="category-list"),
    path("/<str:uid>", CategoryDetailView.as_view(), name="category-detail"),
]