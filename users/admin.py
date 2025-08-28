# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    # Fields to display in list view
    list_display = (
        "email",
        "name",
        "role",
        "is_superuser",
        "is_verified",
        "is_staff",
        "is_active",
        "joined_at",
    )
    list_filter = (
        "role",
        "is_superuser",
        "is_verified",
        "is_staff",
        "is_active",
        "joined_at",
    )
    search_fields = ("email", "name", "phone_number")
    ordering = ("-joined_at",)

    # Fields for editing users
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("name", "phone_number", "profile_picture_url", "location")},
        ),
        (_("Role"), {"fields": ("role",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "joined_at")}),
    )

    # Fields for adding users
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "role",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )
