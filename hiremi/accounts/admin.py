from django.contrib import admin

from .models import Account, City, EmailOTP, State, PasswordResetOTP

# Register your models here.
admin.site.register(Account)
admin.site.register(EmailOTP)
admin.site.register(PasswordResetOTP)
admin.site.register(State)
admin.site.register(City)
