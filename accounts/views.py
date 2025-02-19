# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import User, Notification
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, ProfileSerializer, RefreshTokenSerializer, \
    NotificationSerializer
from django.contrib.auth.hashers import check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
import logging

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Initialize logger
logger = logging.getLogger(__name__)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email_or_username = serializer.validated_data['email_or_username']
            password = serializer.validated_data['password']

            logger.info(f"Attempting login for: {email_or_username}")
            print(email_or_username)
            print(password)

            user = None
            try:
                # Determine if the input is an email or username
                try:
                    validate_email(email_or_username)
                    logger.info("Input detected as email")
                    user = get_user_model().objects.get(email=email_or_username)
                except ValidationError:
                    logger.info("Input detected as username")
                    user = get_user_model().objects.get(username=email_or_username)

                # Validate the password manually
                if not check_password(password, user.password):
                    logger.error("Password does not match")
                    return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

                logger.info(f"Authentication successful for: {user.username}")

                try:
                    Notification.objects.create(
                        user=user,
                        title="Login Successful",
                        content="You have successfully logged in!"
                    )
                except Exception as e:
                    logger.error(f"Failed to create notification: {e}")

                # Generate tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "User logged in successfully",
                    "user_id": str(user.id),
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }, status=status.HTTP_200_OK)
            except get_user_model().DoesNotExist:
                logger.error("No user found with provided email/username")
                return Response({"message": "Invalid email or username"}, status=status.HTTP_401_UNAUTHORIZED)

        logger.error(f"Invalid serializer data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, context={"request": request})  # Ensures absolute URLs for images
        return Response(serializer.data)

    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refreshToken']

        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)

            return Response({
                "success": True,
                "message": "Access token refreshed successfully",
                "accessToken": new_access_token
            }, status=status.HTTP_200_OK)

        except Exception:
            return Response({
                "success": False,
                "message": "Invalid refresh token"
            }, status=status.HTTP_403_FORBIDDEN)


class NotificationListView(APIView):
    def get(self, request):
        user = request.user  # Assuming the user is authenticated

        # Get all notifications for the user, ordered by the latest
        notifications = Notification.objects.filter(user=user).order_by('-created_at')

        # Serialize the notifications
        serializer = NotificationSerializer(notifications, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationReadView(APIView):
    def patch(self, request, notification_id):
        try:
            # Get the notification for the user
            notification = Notification.objects.get(id=notification_id, user=request.user)

            # Mark the notification as read by updating the is_read field
            notification.is_read = True
            notification.save()

            return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'message': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow anyone to request a password reset

    def post(self, request):
        email = request.data.get("email")

        # Check if the user exists with that email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate a reset token (you can customize token generation here)
        reset_code = get_random_string(length=6, allowed_chars='0123456789')

        # Save the reset code (you can store this in the User model or a dedicated ResetCode model)
        user.password_reset_code = reset_code  # Ensure you have a field for storing the reset code
        user.save()

        # Send the reset code to the user's email
        send_mail(
            subject="Password Reset Code",
            message=f"Your password reset code is {reset_code}. Please use this to reset your password.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response({"message": "Password reset code has been sent to your email"}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow anyone to reset password if they have the code

    def post(self, request):
        email = request.data.get("email")
        reset_code = request.data.get("reset_code")
        new_password = request.data.get("new_password")

        # Validate inputs
        if not email or not reset_code or not new_password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the reset code matches
        if user.password_reset_code != reset_code:
            return Response({"error": "Invalid reset code"}, status=status.HTTP_400_BAD_REQUEST)

        # Reset the user's password
        user.password = make_password(new_password)
        user.password_reset_code = ""  # Clear the reset code after use
        user.save()

        return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)