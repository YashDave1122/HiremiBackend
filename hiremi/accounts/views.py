from django.contrib.auth import authenticate, get_user_model, logout
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Account, Education, EmailOTP
from .permissions import IsOwner, IsOwnerOrReadOnly, IsSelf, IsSelfOrReadOnly
from .serializers import (AccountLoginSerializer, AccountRegisterSerializer,
                          AccountSerializer, EducationSerializer,
                          GenerateOTPSerializer, VerifyOTPSerializer)
from .utils import (generate_refresh_response, generate_token_response,
                    send_login_otp_to_email, send_verification_otp_to_email)

User = get_user_model()


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return AccountRegisterSerializer
        if self.action == "generate_otp":
            return GenerateOTPSerializer
        if self.action == "verify_otp":
            return VerifyOTPSerializer
        if self.action == "login":
            return AccountLoginSerializer
        if self.action == "refresh_token":
            return TokenRefreshSerializer
        return AccountSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        if self.action in ["update", "destroy"]:
            return [IsSelfOrReadOnly()]
        return [AllowAny()]

    def create(self, request):
        serializer = AccountRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Remove the OTP after successful registration
        email = serializer.validated_data["email"]
        email_otp = EmailOTP.objects.filter(email=email).order_by("-created_at").first()
        email_otp.delete()

        refresh = RefreshToken.for_user(user)
        return generate_token_response(user, refresh)

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = AccountLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        if user.role == User.SUPER_ADMIN:
            email_otp = (
                EmailOTP.objects.filter(email=user.email).order_by("created_at").first()
            )
            if not email_otp:
                email_otp = EmailOTP.objects.create(email=user.email)
                email_otp.refresh_otp()
                send_login_otp_to_email(user, email_otp.otp)
                return Response("OTP sent to email", status=status.HTTP_200_OK)

            if not email_otp.is_valid():
                email_otp.delete()
                return Response(
                    "OTP expired, request a new one", status=status.HTTP_400_BAD_REQUEST
                )

            # OTP verified, delete it
            email_otp.delete()

        refresh = serializer.validated_data["refresh"]
        return generate_token_response(user, refresh)

    @action(detail=False, methods=["post"])
    def resend_login_otp(self, request):
        email = request.data["email"]
        password = request.data["password"]
        user = authenticate(email=email, password=password)

        if user:
            email_otp = (
                EmailOTP.objects.filter(email=user.email).order_by("created_at").first()
            )
            if not email_otp:
                email_otp = EmailOTP.objects.create(email=user.email)
            email_otp.refresh_otp()
            send_login_otp_to_email(user, email_otp.otp)

            return Response("OTP resent to email", status=status.HTTP_200_OK)

        return Response(
            "Incorrect email or password", status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except:
                pass

        response = Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

    @action(detail=False, methods=["post"])
    def generate_otp(self, request):
        serializer = GenerateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        otp_instance, created = EmailOTP.objects.get_or_create(email=email)

        if not created and not otp_instance.can_be_regenerated():
            return Response(
                {"message": "Wait 2 minutes before requesting another OTP"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        # Update existing OTP or create a new one
        otp = otp_instance.refresh_otp()
        send_verification_otp_to_email(email, otp)
        return Response(
            {"message": "OTP sent to email."}, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def verify_otp(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.validated_data.get("email_otp")
        instance.is_verified = True
        instance.save()

        return Response({"message": "OTP verified"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def refresh_token(self, request):
        old_refresh_token = request.COOKIES.get("refresh_token") or request.data.get(
            "refresh"
        )
        try:
            RefreshToken(old_refresh_token)
        except:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TokenRefreshSerializer(data={"refresh": old_refresh_token})
        try:
            if serializer.is_valid():
                data = serializer.validated_data
                response = generate_refresh_response(data)
                return response
        except:
            return Response(
                {"error": "Invalid Refresh Token"}, status=status.HTTP_400_BAD_REQUEST
            )


class EducationViewSet(viewsets.ModelViewSet):
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
