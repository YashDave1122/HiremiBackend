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

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
                return super().get_queryset()
        return Notification.objects.filter(user= user)
                




   