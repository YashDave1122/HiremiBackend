from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import AccountRegisterSerializer, AccountLoginSerializer, AccountSerializer
from .validators import custom_validation,validate_password


class AccountRegister(APIView):
    permission_classes = (AllowAny,)
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
    permission_classes = (AllowAny,)
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

