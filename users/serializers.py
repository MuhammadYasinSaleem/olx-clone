from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Use email instead of username
        credentials = {"email": attrs.get("email"), "password": attrs.get("password")}

        # This will authenticate using email
        return super().validate(credentials)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role

        return token


class SafeUserSerializer(serializers.ModelSerializer):
    """
    Safe serializer for public user data (when viewing other users)
    """

    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "role_display", "joined_at")
        read_only_fields = ("id", "name", "role_display", "joined_at")


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user's own profile (includes private data)
    """

    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "phone_number",
            "role",
            "role_display",
            "profile_picture_url",
            "joined_at",
            "location",
            "is_verified",
            "is_active",
            "last_login",
        )
        read_only_fields = (
            "id",
            "email",
            "joined_at",
            "is_active",
            "last_login",
            "role_display",
            "is_verified",
            "role",
        )  # Make role read-only


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer for admin use only (includes all fields)
    """

    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "phone_number",
            "role",
            "role_display",
            "profile_picture_url",
            "joined_at",
            "location",
            "is_verified",
            "is_active",
            "last_login",
            "is_staff",
            "is_superuser",
        )
        read_only_fields = ("id", "joined_at", "last_login")


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        help_text="Password must be at least 8 characters long",
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        help_text="Please confirm your password",
    )
    role = serializers.ChoiceField(
        choices=[(User.Role.BUYER, "Buyer"), (User.Role.SELLER, "Seller")],
        required=False,
    )

    class Meta:
        model = User
        fields = ("email", "password", "password_confirm", "role")
        extra_kwargs = {
            "email": {"help_text": "Your email address will be used for login"},
            "role": {"required": False},
        }

    def validate_email(self, value):
        """
        Validate that email is unique and properly formatted
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate(self, attrs):
        """
        Validate the entire registration data
        """
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Password fields didn't match."}
            )

        # Remove password_confirm from validated data as it's not a model field
        attrs.pop("password_confirm")

        return attrs

    def create(self, validated_data):
        """
        Create a new user with the validated data
        """
        password = validated_data.pop("password")

        # Role is optional → set default if not provided
        role = validated_data.get("role", User.Role.BUYER)
        validated_data["role"] = role

        return User.objects.create_user(password=password, **validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile (excludes sensitive fields)
    """

    class Meta:
        model = User
        fields = ("name", "phone_number", "profile_picture_url", "location")
        extra_kwargs = {
            "name": {"required": False},
            "phone_number": {"required": False},
            "profile_picture_url": {"required": False},
            "location": {"required": False},
        }
