import factory
from factory.django import DjangoModelFactory
from .models import CategoryGroup, Category


class CategoryGroupFactory(DjangoModelFactory):
    class Meta:
        model = CategoryGroup

    name = factory.Iterator(["electronics", "furniture", "clothing", "books", "toys"])
    icon = factory.Iterator(["electronics", "furniture", "clothing", "books", "toys"])

    @classmethod
    def create_with_categories(cls, num_categories=3, **kwargs):
        """Create a group with associated categories"""
        group = cls.create(**kwargs)
        for i in range(num_categories):
            CategoryFactory(group=group, name=f"{group.name} Category {i + 1}")
        return group


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    group = factory.SubFactory(CategoryGroupFactory)

    @classmethod
    def create_for_group(cls, group, num_categories=3, **kwargs):
        """Create multiple categories for a specific group"""
        categories = []
        for i in range(num_categories):
            category = cls.create(
                group=group, name=f"{group.name} Item {i+1}", **kwargs
            )
            categories.append(category)
        return categories
