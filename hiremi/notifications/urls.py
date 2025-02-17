from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserNotificationViewSet

# Router for handling notifications per user
router = SimpleRouter()
router.register(r'accounts/(?P<userid>\d+)/notifications', UserNotificationViewSet, basename='user-notifications')

urlpatterns = [
    path('', include(router.urls)),  # Include router-generated URLs
]












# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import NotificationViewSet

# # Create a router and register the NotificationViewSet
# router = DefaultRouter()
# router.register(r'', NotificationViewSet, basename='notifications')  # This handles all CRUD routes

# urlpatterns = [
#     path('', include(router.urls)),  # Includes all routes for NotificationViewSet
# ]
