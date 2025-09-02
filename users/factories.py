import factory
import random
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from locations.factories import LocationFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    name = factory.Faker("name")
    phone_number = factory.LazyAttribute(
        lambda _: f"+1{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
    )
    profile_picture_url = factory.Faker("image_url")
    location = factory.SubFactory(LocationFactory)
    is_verified = factory.Faker("boolean", chance_of_getting_true=70)
    role = factory.Iterator([User.Role.BUYER, User.Role.SELLER])
    is_active = True
    is_staff = False
    password = factory.PostGenerationMethodCall("set_password", "testpass123")

    @classmethod
    def create_buyer(cls, **kwargs):
        return cls(role=User.Role.BUYER, **kwargs)

    @classmethod
    def create_seller(cls, **kwargs):
        return cls(role=User.Role.SELLER, **kwargs)

    @classmethod
    def create_verified_user(cls, **kwargs):
        return cls(is_verified=True, **kwargs)
