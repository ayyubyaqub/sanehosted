from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from accounts.manager import UserManager
from .manager import UserManager
from django.dispatch import receiver
from django.core.mail import send_mail
import uuid
from django.conf import settings


class User(AbstractUser):
    username=None
    first_name=models.CharField(max_length=50, null=True,blank=True)
    last_name=models.CharField(max_length=50, null  =True,blank=True)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=14,unique=True)
    gender=models.CharField(max_length=50,null=True,blank=True)
    is_email_varified=models.BooleanField(default=False)
    is_phone_varified=models.BooleanField(default=False)
    otp=models.CharField(max_length=6,null=True,blank=True)
    email_varification_token=models.CharField(max_length=200,null=True,blank=True)
    forget_password_token=models.CharField(max_length=100,null=True,blank=True)
    last_login=models.DateTimeField(null=True,blank=True)

    objects=UserManager()

    USERNAME_FIELD= 'email'

    REQUIRED_FIELDS=[]

@receiver(post_save,sender=User)
def send_email_token(sender ,instance , created ,**kwargs):
    if created:
        try:
            subject="Your email needs to be verified"
            message=f'hi click on the link to verify email http://localhost:8000/verify/{uuid.uuid4()}'
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[instance.email]
            send_mail(subject ,message ,email_from , recipient_list)

        except Exception as e:
            print(e)