from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import AccountRegisterSerializer, AccountLoginSerializer, AccountSerializer
from .validators import custom_validation,validate_password
from .models import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import OTPSerializer
from .utils import send_otp_to_email



class AccountRegister(APIView):
    def post(self , request):
        try:
            clean_data = custom_validation(request.data)
            serializer = AccountRegisterSerializer(data = clean_data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.create(clean_data)
                if user:
                    return Response(serializer.data,status = status.HTTP_201_CREATED)
        except ValidationError as e:
            print(str(e))
            return Response({"message":str(e)},status = status.HTTP_400_BAD_REQUEST)

class AccountLogin(APIView):
    def post(self, request):
        try:
            data = request.data
            assert validate_password(data)
            serializer = AccountLoginSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.check_user(data)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': AccountSerializer(user).data,
                    'refresh': str(refresh),
                    'access':str(refresh.access_token),
                    },
                    status = status.HTTP_200_OK)
        except ValidationError as e:
            print(str(e))
            return Response({"message":str(e)},status = status.HTTP_400_BAD_REQUEST)

class AccountListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

   

   #views to handle OTP generation and verification
User = get_user_model()

class GenerateOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            send_otp_to_email(user)
            return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({"message": "OTP verified. Login successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    