from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from programs.models import Program
User = get_user_model()


# Create your models here.
class VerificationAmount(models.Model):
    """
    Only update and read using the get_amount and set_amount methods
    """

    amount = models.IntegerField()

    class Meta:
        # Ensure only one instance of this model exists
        constraints = [
            models.CheckConstraint(check=models.Q(id=1), name="only_one_amount_instance")
        ]

    @classmethod
    def get_amount(cls):
        """
        Returns the amount instance (only one should exist).
        If it doesn't exist, create it with a default amount.
        """
        obj, _ = cls.objects.get_or_create(id=1, defaults={'amount': 100})  # Default amount
        return obj.amount

    @classmethod
    def set_amount(cls, new_amount):
        """
        Sets a new amount.
        Only updates the existing amount (since there's only one instance).
        """
        if new_amount < 0:
            raise ValidationError("amount cannot be negative.")
        obj, created = cls.objects.get_or_create(id=1, defaults={'amount': new_amount})
        if not created:
            obj.amount = new_amount
            obj.save()
        return obj.amount

    def __str__(self):
        return f"Amount: {self.amount}"



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