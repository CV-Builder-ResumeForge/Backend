from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.create_user(
    email="test@example.com",
    username="testuser",
    password="password123",
    first_name="Test",
    last_name="User"
)
print(user.check_password("password123"))  # Should return True
