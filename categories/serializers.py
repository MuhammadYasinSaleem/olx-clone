from rest_framework import serializers
from .models import CategoryGroup, Category


class CategoryGroupSerializer(serializers.ModelSerializer):
    category_count = serializers.IntegerField(
        source="categories.count",
        read_only=True,
        help_text="Number of categories in this group",
    )

    class Meta:
        model = CategoryGroup
        fields = ("id", "name", "icon", "category_count", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at", "category_count")


class CategoryGroupDetailSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = CategoryGroup
        fields = ("id", "name", "icon", "categories", "created_at", "updated_at")

    def get_categories(self, obj):
        categories = obj.categories.all().order_by("name")
        return CategorySerializer(categories, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source="group.name", read_only=True)
    group_icon = serializers.CharField(source="group.icon", read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "group",
            "group_name",
            "group_icon",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "group_name",
            "group_icon",
        )


class CategoryWithGroupSerializer(serializers.ModelSerializer):
    group = CategoryGroupSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "group", "created_at", "updated_at")
