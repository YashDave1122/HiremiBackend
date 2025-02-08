from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
import random
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self, email, password,first_name, last_name, phone_number,role):
        if not email:
            raise ValueError("users must have an email adress")
        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            role=role
        )
        user.set_password(password)

        user.save()
        return user
    
    def create_superuser(self, email, password,first_name, last_name, phone_number):
        user = self.create_user(
            email=self.normalize_email(email),
            password = password,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            role = Account.SUPER_ADMIN
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user

class Account(AbstractBaseUser, PermissionsMixin):

    SUPER_ADMIN = 'Super Admin'
    HR = 'HR'
    APPLICANT = 'Applicant'
    
    ROLE_CHOICES = [
        (SUPER_ADMIN, 'Super Admin'),
        (HR, 'HR'),
        (APPLICANT, 'Applicant')
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    role = models.CharField(max_length=40,choices=ROLE_CHOICES,default=APPLICANT)

    is_active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        'first_name','last_name','phone_number'
    ]

    objects = AccountManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name}"
    

#This model will store the OTPs sent to users and manage their validation
User = get_user_model()

class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="email_otp")
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # OTP is valid for 5 minutes
        return datetime.now() < self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"OTP for {self.user.email}: {self.otp}"

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))