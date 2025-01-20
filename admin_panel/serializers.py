from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import check_password
from accounts.models import User
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Admin Login Serializer
class AdminLoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, max_length=128)

    def validate(self, data):
        email_or_username = data.get("email_or_username")
        password = data.get("password")

        if not email_or_username or not password:
            raise serializers.ValidationError("Both email/username and password are required.")

        # Determine if input is an email or username
        try:
            validate_email(email_or_username)  # Check if it's an email
            user = User.objects.get(email=email_or_username)
        except ValidationError:  # Otherwise, treat it as a username
            user = User.objects.filter(username=email_or_username).first()

        if user is None:
            raise serializers.ValidationError("Invalid email/username or password.")

        # Validate password
        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid email/username or password.")

        # Ensure the user is an admin
        if not user.is_admin:
            raise serializers.ValidationError("You do not have admin privileges.")

        data["user"] = user
        return data




















































# class AdminLoginSerializer(serializers.Serializer):
#     email_or_username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#
#     def validate_email_or_username(self, value):
#         """
#         Validate whether the input is a valid email or username.
#         """
#         try:
#             validate_email(value)
#             logger.info(f"Input '{value}' identified as an email.")
#             return {"type": "email", "value": value}
#         except ValidationError:
#             logger.info(f"Input test '{value}' identified as a username.")
#             return {"type": "username", "value": value}
#
#     def validate(self, data):
#         email_or_username = data.get("email_or_username")
#         password = data.get("password")
#
#         logger.info(f"Attempting to validate input: {email_or_username}")
#
#         # Determine if input is email or username
#         validation_result = self.validate_email_or_username(email_or_username)
#
#         # Log the type for clarity
#         detail_type = validation_result["type"]
#         logger.info(f"Details type is == {detail_type}")
#
#         # Extract only the value (email or username string)
#         username_or_email = validation_result["value"]
#         logger.info(f"Extracted value is: {username_or_email}")
#
#         # Initialize username for authentication
#         username = None
#
#         # Handle email case by looking up the username
#         if detail_type == "email":
#             try:
#                 user = User.objects.get(email=username_or_email)
#                 username = user.username  # Get the username for authentication
#                 logger.info(f"User found with email '{username_or_email}'; using username '{username}'.")
#             except User.DoesNotExist:
#                 logger.warning(f"No user found with email '{username_or_email}'.")
#                 raise serializers.ValidationError("Invalid email or password.")
#         else:
#             # Treat as username directly
#             username = username_or_email
#             logger.info(f"Treating input '{username}' as a username.")
#
#         # Authenticate the user with the extracted username
#         logger.info(f"Authenticating with username '{username}'.")
#         user = authenticate(username=username, password=password)
#
#         if user is None:
#             logger.warning(f"Authentication failed for username '{username}'.")
#             raise serializers.ValidationError("Invalid credentials.")
#
#         # Ensure the user is an admin
#         if not user.is_staff:
#             logger.warning(f"User '{username}' does not have admin privileges.")
#             raise serializers.ValidationError("You do not have admin privileges.")
#
#         # Attach the authenticated user to the validated data
#         data["user"] = user
#         return data

