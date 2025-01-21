from django.urls import path
from .views import AccountRegister, AccountLogin

urlpatterns = [
    path('register/', AccountRegister.as_view(), name = 'register'),
    path('login/', AccountLogin.as_view(), name = 'login'),
]
