from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    # Role choices
    class Role(models.TextChoices):
        ADMIN = "admin", _("Admin")
        BUYER = "buyer", _("Buyer")
        SELLER = "seller", _("Seller")

    # Base fields
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(_("full name"), max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture_url = models.URLField(max_length=512, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(
        "locations.Location", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_verified = models.BooleanField(default=False)

    # Role field
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.BUYER,
    )

    # Django required fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    # Custom manager
    objects = CustomUserManager()

    # Use email as the username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-joined_at"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split()[0] if self.name else self.email

    # Property to check if user is admin
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    # Property to check if user is seller
    @property
    def is_seller(self):
        return self.role == self.Role.SELLER

    # Property to check if user is buyer
    @property
    def is_buyer(self):
        return self.role == self.Role.BUYER

    # Save method to ensure role consistency
    def save(self, *args, **kwargs):
        # If user is superuser, automatically set role to admin
        if self.is_superuser and self.role != self.Role.ADMIN:
            self.role = self.Role.ADMIN

        # If user has admin role, ensure they have staff privileges
        if self.role == self.Role.ADMIN:
            self.is_staff = True

        super().save(*args, **kwargs)
