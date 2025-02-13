from django.core.mail import send_mail
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
    send_mail(subject, message, "your_email@example.com", [user.email])


def send_verification_otp_to_email(email, otp):
    # Send email
    subject = "Your OTP for verification"
    message = f"Hi {email},\n\nYour OTP is: {otp}\n\nIt is valid for 5 minutes."
    send_mail(subject, message, "your_email@example.com", [email])


def generateTokenResponse(user, refresh):
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
