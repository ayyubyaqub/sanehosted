from django.urls import path
from .views import *

urlpatterns=[
    path('register/',RegisterView.as_view()),
    path('verify-otp/',VerifyOtp.as_view()),
    path('Login/',LoginView.as_view()),
]