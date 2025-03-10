import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField

from .managers import AccountManager


# Create your models here.
# class State(models.Model):
#     name = models.CharField(primary_key=True, max_length=50)

#     def __str__(self):
#         return self.name


# class City(models.Model):
#     name = models.CharField(max_length=50)
#     state = models.ForeignKey(
#         State, on_delete=models.SET_NULL, related_name="state_cities", null=True
#     )

#     def __str__(self):
#         return f"{self.name} - {self.state}"

#     class Meta:
#         verbose_name_plural = "cities"
#         unique_together = ["name", "state"]
# #########################################################################
class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def _str_(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)

    # def _str_(self):
    def __str__(self):  # ✅ Correct (double underscores)
        return f"{self.name}, {self.state.name}"


class Account(AbstractBaseUser, PermissionsMixin):
    SUPER_ADMIN = "Super Admin"
    HR = "HR"
    APPLICANT = "Applicant"
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

    ROLE_CHOICES = [(SUPER_ADMIN, SUPER_ADMIN), (HR, HR), (APPLICANT, APPLICANT)]
    GENDER_CHOICES = [(MALE, MALE), (FEMALE, FEMALE), (OTHER, OTHER)]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    current_state = models.ForeignKey(
        State, on_delete=models.SET_NULL, null=True, related_name="state_users"
    )
    current_city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, related_name="city_users"
    )

    phone_number = PhoneNumberField()

    birth_state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="state_born_users",
    )
    birth_city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="city_born_users",
    )
    whatsapp_number = PhoneNumberField(null=True, blank=True)
    current_pincode = models.CharField(max_length=10, null=True, blank=True)

    career_stage = models.CharField(max_length=20, null=True, blank=True)

    is_differently_abled = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=APPLICANT)

    # needed for django admin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "phone_number", "father_name", "gender", "date_of_birth"]

    objects = AccountManager()

    def __str__(self):
        return f"{self.id} - {self.full_name}"


# This model will store the OTPs sent to users and manage their validation
class EmailOTP(models.Model):
    email = models.EmailField(primary_key=True)
    otp = models.CharField(max_length=4, default=None, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def can_be_regenerated(self):
        # OTP can be regenerated after a fixed time limit
        return now() > self.created_at + timedelta(minutes=2)

    def is_valid(self, time_limit=5):
        # Used to check OTP expiry and registration time limit
        return now() < self.created_at + timedelta(minutes=time_limit)

    def __str__(self):
        return f"OTP for {self.email}: {self.otp}"

    @staticmethod
    def generate_otp():
        return str(random.randint(1000, 9999))

    def refresh_otp(self):
        self.otp = self.generate_otp()
        self.created_at = now()
        self.is_verified = False
        self.save()
        return self.otp

class PasswordResetOTP(models.Model):
    email = models.EmailField(primary_key=True)
    otp = models.CharField(max_length=4, default=None, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def can_be_regenerated(self):
        # OTP can be regenerated after a fixed time limit
        return now() > self.created_at + timedelta(minutes=2)

    def is_valid(self, time_limit=5):
        # Used to check OTP expiry and registration time limit
        return now() < self.created_at + timedelta(minutes=time_limit)

    def __str__(self):
        return f"Password reset OTP for {self.email}: {self.otp}"

    @staticmethod
    def generate_otp():
        return str(random.randint(1000, 9999))

    def refresh_otp(self):
        self.otp = self.generate_otp()
        self.created_at = now()
        self.is_verified = False
        self.save()
        return self.otp
