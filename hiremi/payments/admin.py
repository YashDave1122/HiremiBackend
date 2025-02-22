from django.contrib import admin

from .models import VerificationOrder, EnrollmentOrder

# Register your models here.
admin.site.register(VerificationOrder)
admin.site.register(EnrollmentOrder)