# serializers.py
from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'name']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone', 'date_of_birth', 'address']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)  # Accept a single name field

    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        full_name = validated_data.pop('name')
        first_name, last_name = self.split_name(full_name)
        user = User.objects.create_user(
            **validated_data,
            first_name=first_name,
            last_name=last_name
        )
        # Assuming a Profile model exists
        Profile.objects.create(user=user)
        return user

    def split_name(self, name):
        """Split full name into first and last name."""
        parts = name.strip().split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""
        return first_name, last_name


class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, max_length=128)

    def validate(self, data):
        email_or_username = data.get('email_or_username')
        password = data.get('password')

        if not email_or_username or not password:
            raise serializers.ValidationError("Both email/username and password are required.")

        return data


class RefreshTokenSerializer(serializers.Serializer):
    refreshToken = serializers.CharField(required=True)

    def validate_refreshToken(self, value):
        if not value:
            raise serializers.ValidationError("Refresh token cannot be empty.")
        return value