from django.urls import path

from .views import (AccountDetailView, AccountListView, AccountLoginView,
                    AccountLogoutView, AccountRegisterView,
                    CurrentAccountDetailView, GenerateOTPView, RefreshView,
                    VerifyOTPView)

urlpatterns = [
    path("", AccountListView.as_view(), name="account_list"),
    path("<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    path("profile/", CurrentAccountDetailView.as_view(), name="profile"),
    path("login/", AccountLoginView.as_view(), name="login"),
    path("refresh_token/", RefreshView.as_view(), name="refresh_token_view"),
    path("register/", AccountRegisterView.as_view(), name="register"),
    path("generate-otp/", GenerateOTPView.as_view(), name="generate_otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path("logout/", AccountLogoutView.as_view(), name="logout"),
]
