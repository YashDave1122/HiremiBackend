from django.contrib.auth import authenticate, get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumbers import NumberParseException, is_valid_number, parse
from rest_framework import exceptions, serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Education, EmailOTP

User = get_user_model()


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
            raise ValidationError({"message": "Choose another email"})

        email_otp = EmailOTP.objects.filter(email=email).order_by("-created_at").first()

        if not email_otp or not email_otp.is_verified:
            raise serializers.ValidationError({"email": "Email not verified."})

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
            raise serializers.ValidationError("Invalid email or password.")

        if user.role == User.SUPER_ADMIN:
            email_otp = EmailOTP.objects.filter(email=email).first()

            if not email_otp:
                # Generate and send OTP if it doesn't exist
                self.send_otp(user)
                raise exceptions.APIException("OTP sent to email.", code=200)

            if not email_otp.is_valid():
                email_otp.delete()
                raise serializers.ValidationError("OTP expired, request a new one.")

            if not otp:
                raise serializers.ValidationError("Please enter an OTP.")

            if otp != email_otp.otp:
                raise serializers.ValidationError("Invalid OTP.")

            # OTP verified, delete it
            email_otp.delete()

        refresh = RefreshToken.for_user(user)
        return {"user": user, "refresh": refresh}


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


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"
        read_only_fields = ["user"]
