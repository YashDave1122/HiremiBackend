from django.contrib.auth import get_user_model, login, logout
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .models import Account, Education, EmailOTP
from .permissions import IsOwner, IsUser
from .serializers import (AccountLoginSerializer, AccountRegisterSerializer,
                          AccountSerializer, EducationSerializer,
                          GenerateOTPSerializer, VerifyOTPSerializer)
from .utils import (generateTokenResponse, send_login_otp_to_email,
                    send_verification_otp_to_email)

COOKIE_SECURE = False  # True means cookie will only be set for https and not http
COOKIE_MAX_AGE = 60 * 60 * 24


class AccountLoginView(APIView):
    serializer_class = AccountLoginSerializer

    def post(self, request):
        data = request.data
        serializer = AccountLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = serializer.validated_data["refresh"]
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
            logout(request)
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


class AccountListCreateView(ListCreateAPIView):
    queryset = Account.objects.all()

    def post(self, request):
        serializer = AccountRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        email = serializer.validated_data["email"]
        email_otp = EmailOTP.objects.filter(email=email).order_by("-created_at").first()
        email_otp.delete()

        refresh = RefreshToken.for_user(user)
        response = generateTokenResponse(user, refresh)

        return response

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AccountRegisterSerializer
        return AccountSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return []


class AccountRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsUser()]


class GenerateOTPView(APIView):
    serializer_class = GenerateOTPSerializer

    def post(self, request):
        email = request.data.get("email")
        serializer = GenerateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = EmailOTP.objects.filter(email=email).first()

        # timeout logic
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
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.validated_data.get("email_otp")
        instance.is_verified = True
        instance.save()
        return Response(
            {"message": "OTP verified"},
            status=status.HTTP_200_OK,
        )


class EducationViewSet(ModelViewSet):
    serializer_class = EducationSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Education.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.kwargs.get("user_id")
        serializer.save(user_id=user_id)

    def get_permission_classes(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return IsOwner
