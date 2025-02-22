from django.db import models
from django.contrib.auth import get_user_model
from programs.models import Program
User = get_user_model()


# Create your models here.
class VerificationOrder(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='verification_orders')
    amount = models.IntegerField()
    payment_id=models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - VerificationOrder #{self.id} - {'PAID' if self.is_paid else 'unpaid'}"

class EnrollmentOrder(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='enrollment_orders')
    amount = models.IntegerField()
    payment_id=models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    program=models.ForeignKey(Program, on_delete=models.PROTECT, related_name='orders')

    def __str__(self):
        return f"{self.user.full_name} - EnrollmentOrder #{self.id} - {'PAID' if self.is_paid else 'unpaid'}"