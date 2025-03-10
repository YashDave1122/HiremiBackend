from django.contrib.auth import authenticate, get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import City, EmailOTP, PasswordResetOTP, State

User = get_user_model()


# class StateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = State
#         fields = "__all__"


# class CitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = City
#         fields = "__all__"

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        # fields = ['name'] 
        fields = "__all__"

class CitySerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='state.name')  # State ko direct naam me convert karo

    class Meta:
        model = City
        # fields = ['id', 'name', 'state']
        fields = "__all__"


class AccountRegisterSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(required=True)

    class Meta:
        model = User
        exclude = [
            "is_superuser",
            "is_staff",
            "is_verified",
            "date_joined",
            "last_login",
            "is_active",
            "groups",
            "user_permissions",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if len(password) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be atleast 8 characters"}
            )

        if not email or User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"message": "Choose another email"})

        email_otp = EmailOTP.objects.filter(email=email).order_by("-created_at").first()

        #if not email_otp or not email_otp.is_verified:
        #    raise serializers.ValidationError({"email": "Email not verified."})

        if role == User.SUPER_ADMIN:
            raise serializers.ValidationError(
                {"role": "Super admin can't register this way"}
            )

        return super().validate(data)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ["groups", "user_permissions", "password"]
        extra_kwargs = {
            "is_verified": {"read_only": True},
            "id": {"read_only": True},
            "last_login": {"read_only": True},
            "is_superuser": {"read_only": True},
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True},
            "date_joined": {"read_only": True},
            "role": {"read_only": True},
        }


class AccountLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    otp = serializers.CharField(max_length=4, required=False)

    class Meta:
        fields = ["email", "password", "otp"]

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        otp = data.get("otp", None)

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Incorrect email or password.")

        email_otp = EmailOTP.objects.filter(email=email).order_by("-created_at").first()
        if email_otp and user.role == User.SUPER_ADMIN:
            if not otp:
                raise serializers.ValidationError("Please enter an OTP.")

            if otp != email_otp.otp:
                raise serializers.ValidationError("Invalid OTP.")

        refresh = RefreshToken.for_user(user)
        return {"user": user, "refresh": refresh}


class AccountLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=150, required=False)


class GenerateOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ["email"]

    def validate(self, data):
        email = data.get("email")
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            raise serializers.ValidationError("User already exists")
        return super().validate(data)


class VerifyOTPSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailOTP
        fields = ["email", "otp"]

    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=4, required=True)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        email_otp = EmailOTP.objects.filter(email=email).order_by("-created_at").first()

        if not email_otp:
            raise serializers.ValidationError({"email": "No OTP for that email"})

        if email_otp.otp != otp:
            raise serializers.ValidationError({"otp": "Invalid OTP"})

        if not email_otp.is_valid():
            raise serializers.ValidationError({"otp": "OTP expired, request a new one"})

        data["email_otp"] = email_otp
        return data


class GeneratePasswordResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ["email"]

    def validate(self, data):
        email = data.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User does not exist")
        data["user"] = user
        return data


class VerifyPasswordResetOTPSerializer(serializers.ModelSerializer):

    class Meta:
        model = PasswordResetOTP
        fields = ["email", "otp"]

    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=4, required=True)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        reset_otp = (
            PasswordResetOTP.objects.filter(email=email).order_by("-created_at").first()
        )

        if not reset_otp:
            raise serializers.ValidationError({"email": "No OTP for that email"})

        if reset_otp.otp != otp:
            raise serializers.ValidationError({"otp": "Invalid OTP"})

        if not reset_otp.is_valid():
            raise serializers.ValidationError({"otp": "OTP expired, request a new one"})

        data["reset_otp"] = reset_otp
        return data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )

        if len(password) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be atleast 8 characters"}
            )

        # Check if OTP is verified
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError({"email": "User not found"})

        reset_otp = PasswordResetOTP.objects.filter(
            email=user.email, is_verified=True
        ).first()
        if not reset_otp:
            raise serializers.ValidationError({"otp": "OTP not verified or expired"})

        # Save user instance in context for use in the view
        self.context["user"] = user
        self.context["reset_otp"] = reset_otp

        return data
