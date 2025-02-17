from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserNotificationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet to list, create, retrieve, update, and delete notifications for a specific user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restrict access to notifications of the user specified in the URL.
        Allow only the logged-in user or an admin to access notifications.
        """
        userid = self.kwargs.get("userid")

        # Restrict users to only access their own notifications unless they are admins
        if self.request.user.id != int(userid) and not self.request.user.is_staff:
            return Notification.objects.none()

        return Notification.objects.filter(user__id=userid)

    def perform_create(self, serializer):
        """
        Ensure the notification is created for the specified user in the URL.
        """
        userid = self.kwargs.get("userid")
        user = get_object_or_404(User, id=userid)
        serializer.save(user=user)










