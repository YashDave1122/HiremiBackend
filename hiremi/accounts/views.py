from django.contrib.auth import get_user_model, login, logout
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .models import Account, EmailOTP
from .serializers import (AccountLoginSerializer, AccountRegisterSerializer,
                          AccountSerializer, EmailOTPSerializer)
from .utils import (generateTokenResponse, send_login_otp_to_email,
                    send_verification_otp_to_email)
from .validators import custom_validation, validate_password

REGISTRATION_TIME_LIMIT = 20  # minutes


class AccountRegisterView(APIView):
    def post(self, request):
        try:
            clean_data = custom_validation(request.data)
        except ValidationError as e:
            return Response({"message": e.message}, status=status.HTTP_400_BAD_REQUEST)
        emailed_otp = EmailOTP.objects.filter(email=clean_data.get("email")).first()

        if not emailed_otp:
            return Response(
                {"message": "Email not verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not emailed_otp.is_valid(REGISTRATION_TIME_LIMIT):
            return Response(
                {"message": "Time limit exceeded, verify email again"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not emailed_otp.is_verified:
            return Response(
                {"message": "OTP Invalid"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = AccountRegisterSerializer(data=clean_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        emailed_otp.delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountLoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = AccountLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        otp = data.get("otp")

        email_otp = EmailOTP.objects.filter(email=user.email).first()

        # If OTP does not exist, generate and send a new one
        if not email_otp:
            send_login_otp_to_email(user)
            return Response(
                {"message": "OTP sent to email."},
                status=status.HTTP_201_CREATED,
            )

        # If OTP is expired, return error and delete OTP
        if not email_otp.is_valid():
            email_otp.delete()  # Remove expired OTPs
            return Response(
                {"message": "OTP expired, request a new one"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If OTP is not provided
        if not otp:
            return Response(
                {"message": "Please enter an OTP"},
                status=status.HTTP_206_PARTIAL_CONTENT,
            )

        # If OTP is incorrect
        if otp != email_otp.otp:
            return Response(
                {"message": "Invalid OTP"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # OTP verified, delete it and generate JWT
        email_otp.delete()

        refresh = RefreshToken.for_user(user)
        response = generateTokenResponse(user, refresh)

        return response


class RefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Check for refresh token in request body (for mobile apps)
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            # If mobile didn't send it, check browser cookies
            refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "No refresh token provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.data["refresh"] = refresh_token  # Inject into request

        response = super().post(request, *args, **kwargs)  # Call parent method

        # Extract new tokens from response
        if "access" in response.data:
            access_token = response.data["access"]
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=COOKIE_SECURE,
                samesite="Lax",
                max_age=COOKIE_MAX_AGE,
            )

        if "refresh" in response.data:
            refresh_token = response.data["refresh"]
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=COOKIE_SECURE,
                samesite="Lax",
                max_age=COOKIE_MAX_AGE,
            )

        response["Access-Control-Allow-Credentials"] = "true"

        return response


class AccountLogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token:
                RefreshToken(refresh_token).blacklist()  # Blacklist token

            response = Response(
                {"message": "Logged out successfully"}, status=status.HTTP_200_OK
            )
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response
        except Exception:
            return Response(
                {"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


# views to handle OTP generation and verification
User = get_user_model()


class GenerateOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            return Response(
                {"message": "User with that email already exists"},
                status=status.HTTP_409_CONFLICT,
            )
        otp = EmailOTP.objects.filter(email=email).first()
        if otp:
            if otp.can_be_regenerated():
                otp.delete()
            else:
                return Response(
                    {"message": "wait 2 minutes before requesting another OTP"},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )

        send_verification_otp_to_email(email)
        return Response(
            {"message": "OTP sent to email."}, status=status.HTTP_201_CREATED
        )


class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        email_otp = EmailOTP.objects.filter(email=email).first()
        if not email_otp.otp == otp:
            return Response(
                {"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not email_otp.is_valid():
            return Response(
                {"message": "OTP expired, request new OTP"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        email_otp.is_verified = True
        email_otp.save()
        return Response(
            {"message": "OTP verified"},
            status=status.HTTP_200_OK,
        )


class AccountListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class AccountDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class CurrentAccountDetailView(RetrieveAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
