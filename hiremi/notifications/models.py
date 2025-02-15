from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=255)  # Type of notification (e.g., system, job update, program enrollment)
    heading = models.CharField(max_length=255)
    content = models.CharField(max_length=255)  # The message content
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created

    def __str__(self):
        return f"{self.type} - {self.user.username}"