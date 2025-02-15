from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response

from .models import Account, EmailOTP
from .serializers import AccountSerializer

COOKIE_SECURE = False  # True means cookie will only be set for https and not http
COOKIE_MAX_AGE = 60 * 60 * 24


def send_login_otp_to_email(user, otp):
    # Send email
    subject = "Your OTP for login"
    message = (
        f"Hi {user.full_name},\n\nYour OTP is: {otp}\n\nIt is valid for 5 minutes."
    )
    send_mail(subject, message, None, [user.email])


def send_verification_otp_to_email(email, otp):
    # Send email
    subject = "Your OTP for verification"
    message = f"Hi {email},\n\nYour OTP is: {otp}\n\nIt is valid for 5 minutes."
    send_mail(subject, message, None, [email])


def send_registration_mail(user):
    # Send email
    subject = "Welcome to Hiremi"
    message = f"Congratulations {user.full_name},\n\n Your account has been created."
    html_message = render_to_string("accounts/welcome_email.html", {"user": user})
    send_mail(subject, message, None, [user.email], html_message=html_message)


def send_password_reset_otp_to_email(user, otp):
    # Send email
    subject = "Password Reset OTP"
    message = (
        f"Hi {user.full_name},\n\nYour OTP is: {otp}\n\nIt is valid for 5 minutes."
    )
    send_mail(subject, message, None, [user.email])


def generate_token_response(user, refresh):
    response = Response(
        {
            "user": AccountSerializer(user).data,
            "access_token": str(refresh.access_token),  # For mobile apps
            "refresh_token": str(refresh),
        },
        status=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="access_token",
        value=str(refresh.access_token),
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="Lax",
        max_age=COOKIE_MAX_AGE,
    )
    response.set_cookie(
        key="refresh_token",
        value=str(refresh),
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="Lax",
        max_age=COOKIE_MAX_AGE,
    )

    response["Access-Control-Allow-Credentials"] = "true"
    return response


def generate_refresh_response(data):
    response = Response(data, status=status.HTTP_200_OK)

    # set new tokens in cookies
    if "access" in data:
        response.set_cookie(
            "access_token",
            data["access"],
            httponly=True,
            secure=COOKIE_SECURE,
            samesite="Lax",
        )

    if "refresh" in data:
        response.set_cookie(
            "refresh_token",
            data["refresh"],
            httponly=True,
            secure=COOKIE_SECURE,
            samesite="Lax",
        )

    response["Access-Control-Allow-Credentials"] = "true"

    return response
