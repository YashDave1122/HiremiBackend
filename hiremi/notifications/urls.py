from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, UserNotificationViewSet

# Global router for general notifications
router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),  

]

