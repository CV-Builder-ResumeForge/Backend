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
from admin_panel.serializers import AdminLoginSerializer, BanUnbanUserSerializer, AddUserSerializer
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from accounts.models import Notification
from .permissions import IsSuperAdminUser
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

            # Create a notification for successful login
            try:
                Notification.objects.create(
                    user=user,
                    title="Login Successful",
                    content=f"You have successfully logged in as {user_type}."
                )
            except Exception as e:
                logger.error(f"Failed to create notification: {e}")

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
        # Create a notification for successful registration
        try:
            Notification.objects.create(
                user=user,
                title="Registration Successful",
                content=f"Welcome {user.username}, your account has been successfully created as {user_type}."
            )
        except Exception as e:
            logger.error(f"Failed to create notification: {e}")

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


class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access

    def delete(self, request, user_id):
        # Get the user who needs to be deleted
        user_to_delete = get_object_or_404(User, id=user_id)

        # Get the currently logged-in user (who is making the request)
        current_user = request.user

        # Super Admin Logic
        if current_user.is_super_admin:
            if user_to_delete == current_user:
                return Response({"error": "You cannot delete yourself"}, status=status.HTTP_400_BAD_REQUEST)
            user_to_delete.delete()
            # Create a notification for successful deletion
            try:
                Notification.objects.create(
                    user=current_user,
                    title="User Deleted",
                    content=f"You have successfully deleted the user: {user_to_delete.username} (Super Admin)."
                )
            except Exception as e:
                logger.error(f"Failed to create notification: {e}")

            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        # Admin Logic
        if current_user.is_admin:
            if user_to_delete.is_admin or user_to_delete.is_super_admin:
                return Response({"error": "You do not have permission to delete this user"}, status=status.HTTP_403_FORBIDDEN)
            user_to_delete.delete()
            # Create a notification for successful deletion
            try:
                Notification.objects.create(
                    user=current_user,
                    title="User Deleted",
                    content=f"You have successfully deleted the user: {user_to_delete.username} (Admin)."
                )
            except Exception as e:
                logger.error(f"Failed to create notification: {e}")
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        # If user is not an admin or super admin
        return Response({"error": "You do not have permission to delete users"}, status=status.HTTP_403_FORBIDDEN)


# 🔴 Endpoint to BAN/UNBAN a user
class BanUnbanUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access

    def patch(self, request, user_id):
        user_to_update = get_object_or_404(User, id=user_id)
        current_user = request.user  # Get the user making the request

        # **Super Admin**: Can ban/unban anyone
        if current_user.is_super_admin:
            serializer = BanUnbanUserSerializer(user_to_update, data=request.data, partial=True)
            if serializer.is_valid():
                is_ban = serializer.validated_data.get('is_ban', user_to_update.is_ban)
                user_to_update.is_ban = is_ban
                user_to_update.is_active = not is_ban  # If banned, deactivate the account
                user_to_update.save()

                message = "User has been banned" if is_ban else "User has been unbanned"
                # Create a notification for successful ban/unban action
                try:
                    Notification.objects.create(
                        user=current_user,
                        title="User Banned/Unbanned",
                        content=f"You have successfully {'banned' if is_ban else 'unbanned'} the user: {user_to_update.username} (Super Admin)."
                    )
                except Exception as e:
                    logger.error(f"Failed to create notification: {e}")
                return Response({"message": message}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # **Admin**: Can only ban/unban normal users (not admins or super admins)
        if current_user.is_admin:
            if user_to_update.is_admin or user_to_update.is_super_admin:
                return Response({"error": "You do not have permission to ban/unban this user"}, status=status.HTTP_403_FORBIDDEN)

            serializer = BanUnbanUserSerializer(user_to_update, data=request.data, partial=True)
            if serializer.is_valid():
                is_ban = serializer.validated_data.get('is_ban', user_to_update.is_ban)
                user_to_update.is_ban = is_ban
                user_to_update.is_active = not is_ban  # If banned, deactivate the account
                user_to_update.save()

                message = "User has been banned" if is_ban else "User has been unbanned"
                # Create a notification for successful ban/unban action
                try:
                    Notification.objects.create(
                        user=current_user,
                        title="User Banned/Unbanned",
                        content=f"You have successfully {'banned' if is_ban else 'unbanned'} the user: {user_to_update.username} (Admin)."
                    )
                except Exception as e:
                    logger.error(f"Failed to create notification: {e}")
                return Response({"message": message}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # **Normal User**: Cannot ban/unban anyone
        return Response({"error": "You do not have permission to ban/unban users"}, status=status.HTTP_403_FORBIDDEN)


# 🔴 Endpoint to ADD a new user (Admin decides verification)
class AddUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AddUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create a notification for the admin who created the user
            try:
                Notification.objects.create(
                    user=request.user,  # The admin creating the user
                    title="User Created",
                    content=f"You have successfully created the user: {user.username}."
                )
            except Exception as e:
                logger.error(f"Failed to create notification: {e}")

            return Response(
                {"message": "User created successfully", "user": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access

    def get(self, request):
        # You can add additional filtering based on conditions like active users, etc.
        total_users = User.objects.count()

        return Response({"total_users": total_users}, status=200)
