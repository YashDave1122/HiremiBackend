import razorpay
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decouple import config

from accounts.permissions import IsVerified

from .models import EnrollmentOrder,VerificationOrder
from .serializers import (EnrollmentOrderSerializer, StartEnrollmentPaymentSerializer, 
                        VerificationOrderSerializer, StartVerificationPaymentSerializer)
from .utils import create_razorpay_order, verify_and_save_payment

User = get_user_model()

class StartVerificationPaymentView(APIView):
    #permission_classes=[IsAuthenticated]
    serializer_class = StartVerificationPaymentSerializer
    def post(self, request):
        # request.data is coming from frontend
        serializer = StartVerificationPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        amount = serializer.validated_data.get('amount')
        user = serializer.validated_data.get('user')

        payment = create_razorpay_order(amount)

        # The order object we save in our database (is_paid=False for now)
        order, _ = VerificationOrder.objects.get_or_create(user=user, 
                                            amount=amount, 
                                            payment_id=payment['id'])

        serializer = VerificationOrderSerializer(order)

        data = {
            "payment": payment,
            "order": serializer.data
        }
        return Response(data)


class HandleVerificationPaymentSuccessView(APIView):
    def post(self, request):
        # request.data is coming from frontend
        res = request.data.get("response")
        ord_id = res.get('razorpay_order_id')

        # get order by payment_id which we've created earlier with is_paid=False
        order = VerificationOrder.objects.get(payment_id=ord_id)

        try:
            verify_and_save_payment(order,res)
        except:
            return Response({'error': 'Something went wrong'})

        order.user.is_verified = True
        order.user.save()

        res_data = {
            'message': 'payment successfully received!'
        }

        return Response(res_data)

class StartEnrollmentPaymentView(APIView):
    #permission_classes=[IsAuthenticated]
    serializer_class = StartEnrollmentPaymentSerializer
    def post(self, request):
        # request.data is coming from frontend
        serializer = StartEnrollmentPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data.get('amount')
        user = serializer.validated_data.get('user')
        program = serializer.validated_data.get('program')

        payment = create_razorpay_order(amount)

        # The order object we save in our database (is_paid=False for now)
        order, _ = EnrollmentOrder.objects.get_or_create(user=user, 
                                            amount=amount, 
                                            payment_id=payment['id'],
                                            program=program)

        serializer = EnrollmentOrderSerializer(order)

        data = {
            "payment": payment,
            "order": serializer.data
        }
        return Response(data)


class HandleEnrollmentPaymentSuccessView(APIView):
    def post(self, request):
        # request.data is coming from frontend
        res = request.data.get("response")
        ord_id = res.get('razorpay_order_id')

        # get order by payment_id which we've created earlier with is_paid=False
        order = EnrollmentOrder.objects.get(payment_id=ord_id)

        try:
            verify_and_save_payment(order,res)
        except:
            return Response({'error': 'Something went wrong'})

        order.program.enroll_user(order.user)

        res_data = {
            'message': 'payment successfully received!'
        }

        return Response(res_data)
