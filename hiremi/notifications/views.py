from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response

User = get_user_model()

class NotificationViewSet(viewsets.ModelViewSet):
  
    """  Handles global notifications (All users). """
   
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated]


class UserNotificationViewSet(viewsets.ModelViewSet):
    
    """ Handles user-specific notifications."""
    
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
      
        " Allow only the logged-in user or an admin to access notifications."
        
        user_id = self.kwargs.get("user_id")

        if self.request.user.id != int(user_id) and not self.request.user.is_staff:
            return Notification.objects.none()

        return Notification.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        
        " Ensure the notification is created for the specified user in the URL."
        
        user_id = self.kwargs.get("user_id")
        user = get_object_or_404(User, id=user_id)
        serializer.save(user=user)

    def user_notifications(self, request, user_id):
        
        if request.user.id != int(user_id) and not request.user.is_staff:
            return Response({"error": "Unauthorized access"}, status=403)

        queryset = Notification.objects.filter(user_id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



