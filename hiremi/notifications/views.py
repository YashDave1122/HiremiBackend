from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing, creating, retrieving, updating, and deleting notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)  # Restrict to logged-in user's notifications

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Assign the notification to the logged-in user
