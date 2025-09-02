from rest_framework import generics, permissions
from .models import CategoryGroup, Category
from .serializers import (
    CategoryGroupSerializer,
    CategoryGroupDetailSerializer,
    CategorySerializer,
    CategoryWithGroupSerializer,
)


class CategoryGroupList(generics.ListAPIView):
    """List all category groups"""

    queryset = CategoryGroup.objects.all().prefetch_related("categories")
    serializer_class = CategoryGroupSerializer
    permission_classes = [permissions.AllowAny]


class CategoryGroupDetail(generics.RetrieveAPIView):
    """Get specific category group with its categories"""

    queryset = CategoryGroup.objects.all().prefetch_related("categories")
    serializer_class = CategoryGroupDetailSerializer
    permission_classes = [permissions.AllowAny]


class CategoryGroupCreate(generics.CreateAPIView):
    """Create new category group (Admin only)"""

    queryset = CategoryGroup.objects.all()
    serializer_class = CategoryGroupSerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryList(generics.ListAPIView):
    """List all categories"""

    queryset = Category.objects.all().select_related("group")
    serializer_class = CategoryWithGroupSerializer
    permission_classes = [permissions.AllowAny]


class CategoryDetail(generics.RetrieveAPIView):
    """Get specific category"""

    queryset = Category.objects.all().select_related("group")
    serializer_class = CategoryWithGroupSerializer
    permission_classes = [permissions.AllowAny]


class CategoryCreate(generics.CreateAPIView):
    """Create new category (Admin only)"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class CategoriesByGroup(generics.ListAPIView):
    """Get all categories for a specific group"""

    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        group_id = self.kwargs["group_id"]
        return Category.objects.filter(group_id=group_id).select_related("group")
