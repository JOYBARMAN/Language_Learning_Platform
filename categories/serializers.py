from rest_framework import serializers

from categories.models import Department, Category


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "uid",
            "name",
            "description",
            "image",
        ]
        read_only_fields = ["uid"]


class CategorySerializer(serializers.ModelSerializer):
    # departments = DepartmentSerializer(
    #     read_only=True, many=True
    # )

    class Meta:
        model = Category
        fields = [
            "uid",
            "name",
            "description",
            "image",
            # "departments",
        ]
        read_only_fields = ["uid"]
