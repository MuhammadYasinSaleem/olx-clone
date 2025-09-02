from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "name",
        "role",
        "phone_number",
        "location",
        "is_superuser",
        "is_verified",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = (
        "role",
        "is_superuser",
        "is_verified",
        "is_staff",
        "is_active",
        "date_joined",
    )
    search_fields = ("email", "name", "phone_number")
    ordering = ("-date_joined",)

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
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

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
