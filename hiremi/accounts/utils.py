from django.core.mail import send_mail
from .models import EmailOTP

def send_otp_to_email(user):
    # Generate or update OTP
    otp, created = EmailOTP.objects.get_or_create(user=user)
    otp.otp = EmailOTP.generate_otp()
    otp.save()

    # Send email
    subject = "Your OTP for Login"
    message = f"Hi {user.full_name},\n\nYour OTP is: {otp.otp}\n\nIt is valid for 5 minutes."
    send_mail(subject, message, 'your_email@example.com', [user.email])
