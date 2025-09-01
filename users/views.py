from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
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

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(
            {
                "message": "Profile updated successfully",
                "data": UserUpdateSerializer(self.request.user).data,
            }
        )
