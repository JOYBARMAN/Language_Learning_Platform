from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from categories.serializers import CategorySerializer, DepartmentSerializer

from categories.models import Category, Department


class CategoryView(ListCreateAPIView):
    serializer_class = CategorySerializer

    # def get_queryset(self):
    #     return Category.objects.filter().prefetch_related("departments")
    def get_queryset(self):
        return Category.objects.filter()


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    lookup_field = "uid"
    queryset = Category.objects.all()


class DepartmentView(ListCreateAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.filter()
