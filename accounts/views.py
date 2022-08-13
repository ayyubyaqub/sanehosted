from ast import Pass
from requests import Response
from rest_framework.serializers import Serializer
from .models import *
from .serializers import *
from rest_framework.views import APIView 
from django.http import JsonResponse
from .helpers import *
from django.contrib.auth import login #authenticate
from rest_framework import status
from django.db.models import Q


def authenticate(username=None, password=None,):
    try:
        user = User.objects.get(
            (Q(email=username) | Q(phone=username)))
        print(user,18)    
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user
        else:
            return None


class  RegisterView(APIView):
    def post(self,request):
        print('i am here 30')
        try:
            serializer=UserSerializer(data=request.data)
            if not serializer.is_valid():
                print(16)
                return JsonResponse(
                    {
                        'status':403,
                        'errors':serializer.errors
                    }
                )
            print(16)
            serializer.save()
            return JsonResponse(
                    {
                        'status':200, 
                        'msg':'an email and otp send on your email and number'
                     }
                )
        except Exception as e :
            print(32)
            print(e)    
            return JsonResponse(
                {
                    'status':404,
                    'error':'something went wrong'
                }
            )

class LoginView(APIView):
    def get(self , request):
        if request.user.is_authenticated:
            userserializer=UserSerializer(request.user)
            return JsonResponse({'status':True,'user_data':userserializer.data})
        return JsonResponse({'status':False})

    def post(self, request, format=None):
        data = request.data
        print(data)
        username = data.get('username', None)
        password = data.get('password', None)
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        print(user,16)
        if user is not None:
            if user.is_active:
                login(request, user)
                userserializer=UserSerializer(user)
                print(userserializer.data)
                return JsonResponse({'status':True,'user_data':userserializer.data})
            else:
                return JsonResponse({
                    'status':False,
                    'msg':'Invalid crediential'
                })    

        else:
            return JsonResponse({
                    'status':False,
                    'error':'something went wrong ayyub'
                })  
    
class VerifyOtp(APIView):
    def post(self, request):
        try:
            data=request.data
            print(data)
            user_obj=User.objects.get(phone=data.get('phone'))
            otp=data.get('otp')
            print(otp)

            if user_obj.otp == otp:
                user_obj.is_phone_varified=True
                user_obj.save()
                userserializer=UserSerializer(user_obj)
                return JsonResponse({'status':True,'user_data':userserializer.data})
            return JsonResponse({
                    'status':403,
                    'msg':'your otp is wrong'
                })    

        except Exception as e:
            print(e)  
        return  JsonResponse({
                    'status':404,
                    'error':'something went wrong'
                })          

    def patch(self, request):
        try :
            data=request.data
            user_obj=User.objects.filter(phone=data.get('phone'))
            if not user_obj.exists():
                return JsonResponse({
                    'status':404,
                    'error':'something went wrong'
                })

            status,time=  send_otp_mobile(data.get('phone'),user_obj[0])  
            if status:
                return JsonResponse({
                    'status':200,
                    'msg':'new otp sent'
                })
            return JsonResponse({
                    'status':404,
                    'error':f'try after {time} seconds'
                })    
        except Exception as e:
            print(e)