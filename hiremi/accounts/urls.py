from django.urls import path
from .views import *
from .views import AccountRegister, AccountLogin, AccountListView, GenerateOTPView, VerifyOTPView

urlpatterns = [
    
    path('register/', AccountRegister.as_view(), name='register'),
    path('login/', AccountLogin.as_view(), name='login'),
    path('users/', AccountListView.as_view(), name='user-list'),
    path('generate-otp/', GenerateOTPView.as_view(), name='generate-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]






