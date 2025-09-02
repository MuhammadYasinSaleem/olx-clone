from django.core.management.base import BaseCommand
from categories.factories import CategoryGroupFactory, CategoryFactory
from categories.models import CategoryGroup, Category


class Command(BaseCommand):
    help = "Seed the database with sample category groups and categories"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all existing categories and groups before seeding",
        )
        parser.add_argument(
            "--groups",
            type=int,
            default=5,
            help="Number of category groups to create (default: 5)",
        )
        parser.add_argument(
            "--categories",
            type=int,
            default=5,
            help="Number of categories per group (default: 5)",
        )

    def handle(self, *args, **options):
        clear = options["clear"]
        num_groups = options["groups"]
        num_categories = options["categories"]

        if clear:
            self.stdout.write("Clearing all categories and groups...")
            Category.objects.all().delete()
            CategoryGroup.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All categories and groups cleared!"))

        self.stdout.write(
            f"Creating {num_groups} groups with {num_categories} categories each..."
        )

        created_groups = 0
        created_categories = 0

        for i in range(num_groups):
            group = CategoryGroupFactory()
            created_groups += 1
            self.stdout.write(f"✓ Created group: {group.name}")

            categories = CategoryFactory.create_for_group(
                group=group, num_categories=num_categories
            )
            created_categories += len(categories)
            for cat in categories:
                self.stdout.write(f"  - Created category: {cat.name}")

        total_groups = CategoryGroup.objects.count()
        total_categories = Category.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"\n Successfully created {created_groups} groups and {created_categories} categories!\n"
                f"Total groups: {total_groups}\n"
                f"Total categories: {total_categories}\n"
            )
        )
