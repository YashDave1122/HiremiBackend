from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

from phonenumber_field.modelfields import PhoneNumberField

USER_MODEL = get_user_model()

class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = '__all__'

    def create(self,clean_data):
        user_obj = USER_MODEL.objects.create_user(email= clean_data['email'],password= clean_data['password'],
                                                  first_name = clean_data['first_name'], last_name = clean_data['last_name'],
                                                  phone_number = clean_data['phone_number'],role=clean_data['role'])
        return user_obj

class AccountLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def check_user(self,clean_data):
        user = authenticate(username = clean_data['email'],password=clean_data['password'])
        if not user:
            raise ValidationError('user not found')
        return user

    class Meta:
        model = USER_MODEL
        fields = ('email','password')

class AccountSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = USER_MODEL
        fields = [
            'email', 'first_name', 'last_name', 'phone_number','role',
            'is_active','is_staff', 'is_superuser',
            'date_joined', 'last_login',
        ]