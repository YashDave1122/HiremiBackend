from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Job(models.Model):
    INTERN = "Intern"
    FRESHER = "Fresher"
    EXPERIENCED = "Experienced"

    JOB_TYPES = [
        (INTERN, INTERN),
        (FRESHER, FRESHER),
        (EXPERIENCED, EXPERIENCED),
    ]

    REMOTE = "Remote"
    ONSITE = "Onsite"
    HYBRID = "Hybrid"

    WORK_MODES = [
        (REMOTE, REMOTE),
        (ONSITE, ONSITE),
        (HYBRID, HYBRID),
    ]

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    eligibility = models.TextField(null=False, blank=False)
    about_company = models.TextField(null=False, blank=False)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default=FRESHER)
    work_mode = models.CharField(max_length=10, choices=WORK_MODES, default=ONSITE)

    def __str__(self):
        return self.title


class Application(models.Model):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

    STATUS_CHOICES = [
        (PENDING, PENDING),
        (ACCEPTED, ACCEPTED),
        (REJECTED, REJECTED),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applications"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Application for {self.job.title} - {self.status}"


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Interest(models.Model):
    interest = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interest")

    
    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    interests = models.ManyToManyField(Interest, blank=True)

    def __str__(self):
        return self.user.username
