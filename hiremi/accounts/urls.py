from django.urls import path

from .views import (AccountListCreateView, AccountLoginView, AccountLogoutView,
                    AccountRetrieveUpdateDestroyView, GenerateOTPView,
                    RefreshView, VerifyOTPView)

urlpatterns = [
    path("", AccountListCreateView.as_view(), name="account_list"),
    path(
        "<int:pk>/", AccountRetrieveUpdateDestroyView.as_view(), name="account_detail"
    ),
    path("login/", AccountLoginView.as_view(), name="login"),
    path("logout/", AccountLogoutView.as_view(), name="logout"),
    path("refresh_token/", RefreshView.as_view(), name="refresh_token_view"),
    path("generate_otp/", GenerateOTPView.as_view(), name="generate_otp"),
    path("verify_otp/", VerifyOTPView.as_view(), name="verify_otp"),
]
