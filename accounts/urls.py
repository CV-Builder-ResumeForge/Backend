# urls.py
from django.urls import path
from .views import RegisterView, LoginView, ProfileView, RefreshTokenView, NotificationReadView, NotificationListView, \
    ForgotPasswordView, ResetPasswordView, MarkAllNotificationsAsReadView, UnreadNotificationCountView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),

    path('api/profile/', ProfileView.as_view(), name='profile'),

    path('api/notifications/', NotificationListView.as_view(), name='notification-list'),
    path('api/notifications/<int:notification_id>/read/', NotificationReadView.as_view(), name='notification-read'),
    path('api/notifications/mark-all-read/', MarkAllNotificationsAsReadView.as_view(), name='mark-all-notifications-read'),
    path('api/notifications/unread/count/', UnreadNotificationCountView.as_view(), name='unread-notification-count'),

    path('api/auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),

    path('api/auth/reset-password/', ResetPasswordView.as_view(), name='reset-password'),

    path('api/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]
