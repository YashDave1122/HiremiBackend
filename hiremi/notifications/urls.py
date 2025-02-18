from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, UserNotificationViewSet

# Global router for general notifications
router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),  

    # Custom User-Specific Notification Endpoints
    path('accounts/<int:user_id>/notifications/', UserNotificationViewSet.as_view({'get': 'user_notifications', 'post': 'create'}), name='user-notifications'),
    path('accounts/<int:user_id>/notifications/<int:pk>/', UserNotificationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-notification-detail'),
]


