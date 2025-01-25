from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework import permissions
from accounts.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from admin_panel.serializers import AdminLoginSerializer
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
import logging

logger = logging.getLogger(__name__)


# Admin Login API View
class AdminLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Determine user type (Super Admin or Admin)
            if user.is_super_admin:
                user_type = "SuperAdmin"
            else:
                user_type = "Admin"

            logger.info(f"Login successful for {user.username} as {user_type}.")

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Admin logged in successfully",
                "user_type": user_type,
                "username": user.username,
                "email": user.email,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_200_OK)

        # Log validation errors
        logger.error(f"Login failed with errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAdminAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        # Check if the user making the request is a superadmin
        if not request.user.is_superadmin:
            return Response({"error": "You do not have permission to delete admins"}, status=status.HTTP_403_FORBIDDEN)

        try:
            admin = User.objects.get(pk=pk)
            if admin.is_superadmin:
                return Response({"error": "You cannot delete a superadmin"}, status=status.HTTP_400_BAD_REQUEST)
            admin.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)


class AdminRegisterAPIView(APIView):
    """
    Allows superadmins to create new admins.
    """

    def post(self, request):
        # Ensure the request user is authenticated as a superadmin
        if not request.user.is_authenticated or not request.user.is_superadmin:
            return Response(
                {"error": "Only a superadmin can create an admin."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Extract and validate data from request
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        is_admin = request.data.get('is_admin', False)  # Defaults to False if not provided

        if not username or not password or not email:
            return Response(
                {"error": "Username, email, and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure superadmins cannot create another superadmin
        if request.data.get('is_superadmin', False):
            return Response(
                {"error": "Superadmins cannot create other superadmins."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Create a new admin
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_admin=is_admin,  # Mark as admin if requested
            is_staff=True,  # Grant staff privileges
            is_superadmin=False,  # Ensure it's not a superadmin
        )

        return Response(
            {
                "message": "Admin created successfully!",
                "admin_id": str(user.id),
                "is_admin": user.is_admin,
            },
            status=status.HTTP_201_CREATED,
        )

class UserListView(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can access this view

    def get(self, request):
        users = User.objects.all()  # Fetch all users
        serializer = UserSerializer(users, many=True)  # Serialize multiple users
        return Response(serializer.data)  # Return serialized data