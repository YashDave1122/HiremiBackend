from django.contrib import admin

from .models import Account, EmailOTP, State

# Register your models here.
admin.site.register(Account)
admin.site.register(EmailOTP)
admin.site.register(State)
