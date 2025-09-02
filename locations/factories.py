import factory
from factory.django import DjangoModelFactory
from .models import Location


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location

    name = factory.Faker("city")
