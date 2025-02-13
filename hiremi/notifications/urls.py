from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

# Create a router and register the NotificationViewSet
router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notifications')  # This handles all CRUD routes

urlpatterns = [
    path('', include(router.urls)),  # Includes all routes for NotificationViewSet
]
