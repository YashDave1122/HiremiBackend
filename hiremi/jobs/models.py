from django.db import models

# Create your models here.
class Job(models.Model):
    INTERN = "Intern"
    FRESHER = "Fresher"
    EXPERIENCED = "Experienced"

    JOB_TYPES = [
        (INTERN, INTERN),
        (FRESHER, FRESHER),
        (EXPERIENCED,  EXPERIENCED),
    ]

    REMOTE = "Remote"
    ONSITE = "Onsite"
    HYBRID = "Hybrid"

    WORK_MODES = [
        (REMOTE, REMOTE),
        (ONSITE, ONSITE),
        (HYBRID, HYBRID),
    ]

    

    title = models.CharField(max_length=255)
    description = models.TextField()
    eligibility = models.TextField()
    about_company = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    work_mode = models.CharField(max_length=10, choices=WORK_MODES)
    

    def __str__(self):
        return self.title



# Application Model
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")],
    )

    def __str__(self):
        return f"Application for {self.job.title} - {self.status}"





# Skill Model
class Skill(models.Model):
    name = models.CharField(max_length=100, primary_key=True)  # Set as primary key

    def __str__(self):
        return self.name



# Interest Model
class Interest(models.Model):
    name = models.CharField(max_length=100, primary_key=True)  # Set as primary key

    def __str__(self):
        return self.name
