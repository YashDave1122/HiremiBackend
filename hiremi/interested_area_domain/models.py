# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class SelectedDomain(models.Model):
#     register = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
#     items = models.CharField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def _str_(self):
#         return f"{self.register.email}'s domains"
    

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SelectedDomain(models.Model):
    register = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensure one entry per user
    items = models.CharField(max_length=500)  # Stores selected domains as comma-separated string
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.register.email}'s selected domains"

    def save(self, *args, **kwargs):
        # Ensure no more than 5 domains are selected
        if len(self.items.split(',')) > 5:
            raise ValueError("You can select at most 5 domains.")
        super().save(*args, **kwargs)
