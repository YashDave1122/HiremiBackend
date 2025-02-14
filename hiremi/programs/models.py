
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the user model dynamically

class Program(models.Model):

    # Define static Variable
    ONLINE = 'Online'
    OFFLINE = 'Offline'
    HYBRID = 'Hybrid'


    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    MODE_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Hybrid', 'Hybrid'),
    ]

    name = models.CharField(max_length=255, unique=True)  # Program name
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Program fee
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    description = models.TextField(blank=True, null=True)  # Program description
    duration = models.CharField(max_length=50, null=True, blank=True)
    is_active =  models.CharField(max_length=5,choices=[('Yes', 'Yes'), ('No', 'No')],default='Yes')  # Whether the program is active
    created_at = models.DateTimeField(auto_now_add=True)  # When the program was created
    updated_at = models.DateTimeField(auto_now=True)  # When the program was last updated
    mode_of_learning = models.CharField(max_length=10, choices=MODE_CHOICES, default='Online')  # Online/Offline/Hybrid 
    course_level = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES, default='Beginner')  # Course level
    internship_company = models.CharField(max_length=255, null=True, blank=True)
    enrollment_deadline = models.DateField(null=True, blank=True)  # Last date to enroll
   


    def __str__(self):
        return self.name


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="enrollments")
    date_enrolled = models.DateTimeField(auto_now_add=True)  # When the enrollment was created
    end_date = models.DateField(null=True, blank=True)  # Program end date

 
 # Define static Variable
    PENDING  ='Pending'
    CONFIRMED = 'Confirmed'
    CANCELED = 'Canceled'
    REJECTED = 'Rejected'
   

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Canceled', 'Canceled'),
        ('Rejected','Rejected'),
       
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    PAYMENT_STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
        ('Refunded', 'Refunded'),
    ]
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Unpaid')
    payment_date = models.DateField(null=True, blank=True)
   
  

    def __str__(self):
        return f"{self.user.username} enrolled in {self.program.name}"
