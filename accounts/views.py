# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, ProfileSerializer, RefreshTokenSerializer
from django.contrib.auth.hashers import check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
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
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
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