from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    SafeUserSerializer,
    AdminUserSerializer,
    UserUpdateSerializer,
    CustomTokenObtainPairSerializer,
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = CustomTokenObtainPairSerializer.get_token(user)
        access = refresh.access_token

        return Response(
            {
                "refresh": str(refresh),
                "access": str(access),
            },
            status=status.HTTP_201_CREATED,
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserUpdateSerializer
        return UserProfileSerializer

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        # Use SafeUserSerializer for non-superuser admins, AdminUserSerializer for superusers
        if self.request.user.is_superuser:
            return AdminUserSerializer
        return SafeUserSerializer

    def get_queryset(self):
        # Only admins can see all users
        if self.request.user.is_admin:
            return User.objects.all()
        return User.objects.none()


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        user = self.get_object()
        requester = self.request.user

        # Users can see their own full profile
        if user == requester:
            return UserProfileSerializer

        # Admins can see full profiles of other users
        if requester.is_superuser:
            return AdminUserSerializer

        # Regular users can only see safe info of other users
        return SafeUserSerializer

    def get_queryset(self):
        return User.objects.all()


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def user_role_info(request):
    """Get current user's role information"""
    user = request.user
    return Response(
        {
            "role": user.role,
            "role_display": user.get_role_display(),
            "is_admin": user.is_admin,
            "is_seller": user.is_seller,
            "is_buyer": user.is_buyer,
        }
    )
