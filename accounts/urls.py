from django.urls import path
from .views import *

from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('education_details', educationdetail, basename='educationdetail')
# urlpatterns1 = router.urls

urlpatterns=[
    path('register/',RegisterView.as_view()),
    path('verify-otp/',VerifyOtp.as_view()),
    path('Login/',LoginView.as_view()),
    path('education_details/',educationdetail.as_view()),
    path('education_details/<int:pk>',educationdetail.as_view()),
    path('skill/',skill.as_view()),
    path('skill/<int:pk>',skill.as_view()),
    path('professional_Detail/',professional_Detail.as_view()),
    path('professional_Detail/<int:pk>',professional_Detail.as_view()),
    path('user_project/',user_project_view.as_view()),
    path('user_project/<int:pk>',user_project_view.as_view()),
]