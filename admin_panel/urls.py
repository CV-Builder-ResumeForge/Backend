from django.urls import path
from .views import AdminLoginAPIView, DeleteAdminAPIView, AdminRegisterAPIView

urlpatterns = [
    path('api/login/', AdminLoginAPIView.as_view(), name='admin-login'),
    path('api/delete/<uuid:pk>/', DeleteAdminAPIView.as_view(), name='delete-admin'),
    path('api/delete/<uuid:pk>/', DeleteAdminAPIView.as_view(), name='delete-admin'),
    path('api/register/', AdminRegisterAPIView.as_view(), name='register-admin')
]
