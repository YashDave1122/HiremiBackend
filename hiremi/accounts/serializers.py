from django.contrib.auth import authenticate, get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumbers import NumberParseException, is_valid_number, parse
from rest_framework import serializers

from .models import EmailOTP

User = get_user_model()


class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        ]
        extra_kwargs = {
            "email": {"read_only": True},
            "password": {"write_only": True},
        }


class AccountLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        return {"user": user}


class EmailOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailOTP
        fields = "__all__"
