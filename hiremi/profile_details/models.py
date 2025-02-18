from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import City, State

User = get_user_model()

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="experiences")
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Allows for ongoing jobs
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_links")
    name = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return self.name



class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="educations")
    college_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    college_state = models.ForeignKey(
        State, on_delete=models.SET_NULL, null=True, related_name="state_educations"
    )
    college_city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, related_name="city_educations"
    )

    passing_year = models.IntegerField()
    percentage = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name} {self.degree} {self.college_name}"
