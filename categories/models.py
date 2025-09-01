from django.db import models


class CategoryGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(
        max_length=50, help_text="Icon name for UI (e.g., 'car', 'phone', 'home')"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category Group"
        verbose_name_plural = "Category Groups"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    group = models.ForeignKey(
        CategoryGroup, on_delete=models.CASCADE, related_name="categories"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        unique_together = ["name", "group"]

    def __str__(self):
        return f"{self.name} ({self.group.name})"
