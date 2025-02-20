
from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()

class Query(models.Model):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

    STATUS_CHOICES = [
        (OPEN, OPEN),
        (IN_PROGRESS, IN_PROGRESS),
        (CLOSED, CLOSED),
    ]




    ENGLISH ="english"
    HINDI ="hindi"
    BOTH ="both"

    LANGUAGE_CHOICES = [
        (ENGLISH, ENGLISH),
        (HINDI, HINDI),
        (BOTH, BOTH),
    ]



    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="queries")
    subject = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    query_type = models.CharField(max_length=100, blank=True, null=True)  
    preferred_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default="English")

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.status})"
