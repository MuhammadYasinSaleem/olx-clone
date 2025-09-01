from django.contrib import admin
from .models import CategoryGroup, Category


@admin.register(CategoryGroup)
class CategoryGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "category_count", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "icon")
    readonly_fields = ("created_at", "updated_at")

    def category_count(self, obj):
        return obj.categories.count()

    category_count.short_description = "Categories"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "created_at")
    list_filter = ("group", "created_at")
    search_fields = ("name", "group__name")
    readonly_fields = ("created_at", "updated_at")
