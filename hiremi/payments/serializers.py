from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import VerificationOrder, EnrollmentOrder, VerificationAmount
from programs.models import Program, Enrollment

User = get_user_model()

class VerificationOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerificationOrder
        fields = '__all__'

        read_only_fields = ['order_date']

class EnrollmentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentOrder
        fields = '__all__'
        read_only_fields = ['order_date']

class StartVerificationPaymentSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self,data):
        data['amount'] = VerificationAmount.get_amount()
        user = data.get('user')
        
        if user.is_verified:
            raise serializers.ValidationError("User already verified")
        
        return data
        
        
class StartEnrollmentPaymentSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())
    def validate(self,data):
        user = data.get('user')
        program = data.get('program')
        data['amount'] = program.sale_price or program.price

        if not program:
            raise serializers.ValidationError("Program ID is required for program order")
        
        if user.enrollments.filter(program=program,status=Enrollment.CONFIRMED).exists():
            raise serializers.ValidationError("User already enrolled in this program")
        
        if user.enrollments.filter(program=program,status=Enrollment.PENDING).exists():
            raise serializers.ValidationError("User already applied to enroll in this program")
        
        return data
