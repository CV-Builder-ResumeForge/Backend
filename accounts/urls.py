# urls.py
from django.urls import path
from .views import RegisterView, LoginView, ProfileView, RefreshTokenView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]
