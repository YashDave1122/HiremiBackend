from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AccountListCreateView, AccountLoginView, AccountLogoutView,
                    AccountRetrieveUpdateDestroyView, EducationViewSet,
                    GenerateOTPView, RefreshView, VerifyOTPView)

router = DefaultRouter()
router.register(r"(?P<user_id>\d)/education", EducationViewSet, basename="education")

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
    path(
        "<int:user_id>/education/",
        EducationViewSet.as_view({"get": "list", "post": "create"}),
        name="education-list",
    ),
    path(
        "<int:user_id>/education/<int:pk>/",
        EducationViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="education-detail",
    ),
]
