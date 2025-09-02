from django.core.management.base import BaseCommand
from locations.factories import LocationFactory
from ...models import Location


class Command(BaseCommand):
    help = "Seed the database with random city names"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=20,
            help="Number of city locations to create (default: 20)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all existing locations before seeding",
        )

    def handle(self, *args, **options):
        count = options["count"]
        clear = options["clear"]

        if clear:
            self.stdout.write("Clearing all existing locations...")
            Location.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All locations cleared!"))

        self.stdout.write(f"Creating {count} random city locations...")

        for i in range(count):
            location = LocationFactory()
            self.stdout.write(f"✓ Created: {location.name}")

        total_locations = Location.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {count} locations! "
                f"Total in database: {total_locations}"
            )
        )
