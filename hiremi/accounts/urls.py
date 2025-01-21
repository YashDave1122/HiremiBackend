from django.urls import path
from .views import *

urlpatterns = [
    path('',AccountListView.as_view(),name="account_list"),
    path('register/', AccountRegister.as_view(), name = 'register'),
    path('login/', AccountLogin.as_view(), name = 'login'),

]
