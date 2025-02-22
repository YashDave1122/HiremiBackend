from django.urls import path

from .views import (StartVerificationPaymentView, HandleVerificationPaymentSuccessView,
                    StartEnrollmentPaymentView, HandleEnrollmentPaymentSuccessView)

urlpatterns = [
    path('verify/', StartVerificationPaymentView.as_view(), name="verification_payment"),
    path('verify/success/', HandleVerificationPaymentSuccessView.as_view(), name="verification_payment_success"),
    path('enroll/', StartEnrollmentPaymentView.as_view(), name="enrollment_payment"),
    path('enroll/success/', HandleEnrollmentPaymentSuccessView.as_view(), name="enrollment_payment_success"),
]
