from pyexpat import model
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


class Education_detail(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE,related_name='education_details',null=True,blank=True)
    school_name=models.CharField(max_length=100,null=True,blank=True)
    qualification=models.CharField(max_length=100,null=True,blank=True)
    board=models.CharField(max_length=100,null=True,blank=True)
    field=models.CharField(max_length=100,null=True,blank=True)
    From=models.DateField(null=True, blank=True)
    to=models.DateField(null=True, blank=True)
    grades=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
  

class professional_basic(models.Model):
    pass

class Skill(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='skill')
    skill=models.CharField(max_length=255,null=True,blank=True)


class professional_detail(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE,related_name='professionaldetail',null=True,blank=True)
    company_name=models.CharField(max_length=255,null=True,blank=True)
    designation=models.CharField(max_length=255,null=True,blank=True)
    From=models.DateField(null=True, blank=True)
    to=models.DateField(null=True, blank=True)
    is_currently_working=models.BooleanField(default=False)
    location=models.TextField(null=True,blank=True)
    work_responsibility=models.TextField(null=True,blank=True)


class user_project(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='project')
    project_title=models.CharField(max_length=255,null=True,blank=True)
    project_desc=models.TextField()
    project_link=models.TextField()
