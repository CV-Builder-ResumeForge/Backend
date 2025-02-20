from django.urls import path
from .views import AdminLoginAPIView, AdminRegisterAPIView, UserListView, DeleteUserView, \
    BanUnbanUserView, AddUserView, UserCountView, AdminUserProfileView

urlpatterns = [
    path('api/login/', AdminLoginAPIView.as_view(), name='admin-login'),

    path('api/register/', AdminRegisterAPIView.as_view(), name='register-admin'),

    path('api/allUsersList/', UserListView.as_view(), name='user-list'),

    path('api/users/delete/<uuid:user_id>/', DeleteUserView.as_view(), name='delete-user'),

    path('api/users/ban-unban/<uuid:user_id>/', BanUnbanUserView.as_view(), name='ban-unban-user'),

    path('api/users/add/', AddUserView.as_view(), name='add-user'),

    path('api/users/total/', UserCountView.as_view(), name='user-count'),

    path('api/profile/<uuid:user_id>/', AdminUserProfileView.as_view(), name='admin-user-profile'),
]
