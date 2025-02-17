from django.db import models

class Job(models.Model):
    INTERN = "Intern"
    FRESHER = "Fresher"
    EXPERIENCED = "Experienced"

    JOB_TYPES = [
        (INTERN, "Intern"),
        (FRESHER, "Fresher"),
        (EXPERIENCED, "Experienced"),
    ]

    REMOTE = "Remote"
    ONSITE = "Onsite"
    HYBRID = "Hybrid"

    WORK_MODES = [
        (REMOTE, "Remote"),
        (ONSITE, "Onsite"),
        (HYBRID, "Hybrid"),
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
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending",  
    )

    def __str__(self):
        return f"Application for {self.job.title} - {self.status}"


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
