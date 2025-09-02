import random
from django.core.management.base import BaseCommand
from users.factories import UserFactory
from locations.models import Location
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample users (no admins)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=50,
            help="Number of users to create (default: 50)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all existing regular users before seeding",
        )
        parser.add_argument(
            "--ratio",
            type=str,
            default="70:30",
            help="Ratio of buyers:sellers (default: 70:30)",
        )

    def handle(self, *args, **options):
        count = options["count"]
        clear = options["clear"]
        ratio = options["ratio"]

        buyer_ratio, seller_ratio, total_ratio = self.parse_ratio(ratio)
        if buyer_ratio is None:
            return

        if clear:
            self.clear_users()

        locations = list(Location.objects.all())
        if not locations:
            self.stdout.write(
                self.style.ERROR("No locations found! Please seed locations first.")
            )
            return

        self.stdout.write(f"Creating {count} sample users with ratio {ratio}...")

        buyer_count = int(count * buyer_ratio / total_ratio)
        seller_count = count - buyer_count

        created_count = self.seed_buyers(buyer_count, locations)
        created_count += self.seed_sellers(seller_count, locations)

        self.seed_test_users(locations)

        self.print_summary(created_count)

    def parse_ratio(self, ratio):
        try:
            buyer_ratio, seller_ratio = map(int, ratio.split(":"))
            total_ratio = buyer_ratio + seller_ratio
            return buyer_ratio, seller_ratio, total_ratio
        except (ValueError, AttributeError):
            self.stdout.write(
                self.style.ERROR('Invalid ratio format. Use format like "70:30"')
            )
            return None, None, None

    def clear_users(self):
        self.stdout.write("Clearing regular users...")
        User.objects.filter(role__in=[User.Role.BUYER, User.Role.SELLER]).delete()
        self.stdout.write(self.style.SUCCESS("Regular users cleared!"))

    def seed_buyers(self, count, locations):
        self.stdout.write(f"Creating {count} buyers...")
        created = 0
        for i in range(count):
            UserFactory.create_buyer(location=random.choice(locations))
            created += 1
            if created % 10 == 0:
                self.stdout.write(f"Created {created} users...")
        return created

    def seed_sellers(self, count, locations):
        self.stdout.write(f"Creating {count} sellers...")
        created = 0
        for i in range(count):
            UserFactory.create_seller(
                location=random.choice(locations),
                is_verified=random.choice([True, False]),
            )
            created += 1
            if created % 10 == 0:
                self.stdout.write(f"Created {created} users...")
        return created

    def seed_test_users(self, locations):
        test_users = [
            {
                "email": "buyer@example.com",
                "name": "Test Buyer",
                "role": User.Role.BUYER,
            },
            {
                "email": "seller@example.com",
                "name": "Test Seller",
                "role": User.Role.SELLER,
                "is_verified": True,
            },
            {
                "email": "unverified_seller@example.com",
                "name": "Unverified Seller",
                "role": User.Role.SELLER,
            },
        ]

        self.stdout.write("Creating test users...")
        for test_user in test_users:
            user, created = User.objects.get_or_create(
                email=test_user["email"],
                defaults={
                    "name": test_user["name"],
                    "role": test_user["role"],
                    "is_verified": test_user.get("is_verified", False),
                    "location": random.choice(locations),
                },
            )
            user.set_password("testpass123")
            user.save()

            if created:
                self.stdout.write(f"✓ Created test user: {user.email}")
            else:
                self.stdout.write(f" Test user already exists: {user.email}")

    def print_summary(self, created_count):
        total_users = User.objects.count()
        buyer_total = User.objects.filter(role=User.Role.BUYER).count()
        seller_total = User.objects.filter(role=User.Role.SELLER).count()
        admin_total = User.objects.filter(role=User.Role.ADMIN).count()

        self.stdout.write(
            self.style.SUCCESS(
                f"\n Successfully created {created_count} users!\n"
                f" Total users: {total_users}\n"
                f" Buyers: {buyer_total}\n"
                f" Sellers: {seller_total}\n"
                f" Admins: {admin_total} (not created by seeder)\n"
                f"\nTest users:\n"
                f"• buyer@example.com / testpass123\n"
                f"• seller@example.com / testpass123\n"
                f"• unverified_seller@example.com / testpass123\n"
            )
        )
