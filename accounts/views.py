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
from rest_framework import viewsets
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
        print(request.data)
        try:
            serializer=UserSerializer(data=request.data)
            if not serializer.is_valid():
                print(serializer.errors,34)
                return JsonResponse(
                    {
                        'status':403,
                        'error':str(serializer.errors)
                    }
                )
            print('OK')
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
            print(userserializer.data['id'],12)
            return JsonResponse({'status':True,'user_data':userserializer.data})
        return JsonResponse({'status':False})

    def post(self, request, format=None):
        data = request.data
        print(data)
        username = data.get('username', None)
        password = data.get('login_password', None)
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


class educationdetail(APIView):
    def get(self,request,pk=None):
        print(pk)
        if pk != None:
            print(pk,306)
            skills=Education_detail.objects.filter(user__id=pk)
            skillsdata=Education_detailSerializer(skills,many=True)
            return JsonResponse(
                    {
                        'status':200,
                        'data':skillsdata.data
                        
                    }
                )
        educationdetaildata=Education_detail.objects.all()
        educationdetaildata=Education_detailSerializer(educationdetaildata,many=True)
        return JsonResponse(
                    {
                        'status':200,
                        'data':educationdetaildata.data
                        
                    }
                )

    def post(self,request):
        data=request.data
        print(data)
    
        try:
            serializer=Education_detailSerializer(data=data)
            if not serializer.is_valid():
                print(serializer.errors)
                return JsonResponse(
                    {
                        'status':403,
                        'errors':serializer.errors
                        
                    }
                )
            print('OK')
            resp=serializer.save()
           
            return JsonResponse(
                    {
                        'status':200, 
                        'msg':'Your Education detail is saved'
                     }
                )
        except Exception as e :
            print(178)
            print(e,179)    
            return JsonResponse(
                {
                    'status':404,
                    'error':'something went wrong'
                }
            )
    

    def delete(self, request,pk):
   
        edu_detail=Education_detail.objects.get(id=pk)
        edu_detail.delete()
        return JsonResponse(
                    {
                        'status':200,
                        'data':'congratulations you are in delete'
                        
                    }
                )

    def put(self, request, pk, format=None):
        educationdetail = Education_detail.objects.get(id=pk)
    
        try:
            serializer = Education_detailSerializer(educationdetail, data=request.data)
        except Exception as e:  
            print(e)
            pass
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status':True,'user_data':serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class skill(APIView):
    def get(self,request,pk=None):
        print(304)
        if pk != None:
            print(pk,306)
            skills=Skill.objects.filter(user__id=pk)
            skillsdata=SkillSerializer(skills,many=True)
            return JsonResponse(
                    {
                        'status':200,
                        'data':skillsdata.data
                        
                    }
                )

        skills=Skill.objects.all()
        skillsdata=SkillSerializer(skills,many=True)
        return JsonResponse(
                    {
                        'status':200,
                        'data':skillsdata.data
                        
                    }
                )

    def post(self,request):
        data=request.data 
        print(data)   
        try:
            serializer=SkillSerializer(data=data)
            if not serializer.is_valid():
                print(serializer.errors)
                return JsonResponse(
                    {
                        'status':403,
                        'errors':serializer.errors
                        
                    }
                )
            resp=serializer.save()
           
            return JsonResponse(
                    {
                        'status':200, 
                        'msg':'Your skill detail is saved'
                     }
                )
        except Exception as e :
            print(178)
            print(e,179)    
            return JsonResponse(
                {
                    'status':404,
                    'error':'something went wrong'
                }
            )
    

    def delete(self, request,pk):
        print(pk)   
        skill=Skill.objects.get(id=pk)
        skill.delete()
        return JsonResponse(
                    {
                        'status':200,
                        'data':' your project detail is deleted'
                        
                    }
                )

    def put(self, request, pk, format=None):
        skilldetail = Skill.objects.get(id=pk)
        try:
            serializer = Education_detailSerializer(skilldetail, data=request.data)

        except Exception as e:  
            print(e)
            pass
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status':True,'updated_skill':serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)         




class professional_Detail(APIView):
    def get(self,request,pk=None):
        print(319)
        if pk != None:
            print(pk,321)
            skills=professional_detail.objects.filter(user__id=pk)
            skillsdata=ProfessionalDetailSerializer(skills,many=True)
            return JsonResponse(
                    {
                        'status':200,
                        'data':skillsdata.data
                        
                    }
                )
        
        prof_detail=professional_detail.objects.all()
        skillsdata=ProfessionalDetailSerializer(prof_detail,many=True)
        return JsonResponse(
                    {
                        'status':200,
                        'data':skillsdata.data
                        
                    }
                )

    def post(self,request):
        data=request.data
        print(data)
    
        try:
            serializer=ProfessionalDetailSerializer(data=data)
            if not serializer.is_valid():
                print(serializer.errors)
                return JsonResponse(
                    {
                        'status':403,
                        'errors':serializer.errors
                        
                    }
                )
            resp=serializer.save()
           
            return JsonResponse(
                    {
                        'status':200, 
                        'msg':'Your professional detail is saved'
                     }
                )
        except Exception as e :
            print(178)
            print(e,179)    
            return JsonResponse(
                {
                    'status':404,
                    'error':'something went wrong'
                }
            )
    

    def delete(self, request,pk):
        print(pk)   
        prof_detail=professional_detail.objects.get(id=pk)
        prof_detail.delete()
        return JsonResponse(
                    {
                        'status':200,
                        'data':' your professional detail is deleted'
                        
                    }
                )

    def put(self, request, pk, format=None):
        prof_detail = professional_detail.objects.get(id=pk)
        try:
            serializer = Education_detailSerializer(prof_detail, data=request.data)

        except Exception as e:  
            print(e)
            pass
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status':True,'updated_skill':serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)         



class user_project_view(APIView):
    def get(self,request,pk=None):
        print(406)
        if pk != None:
            print(pk,408)
            userproject=user_project.objects.filter(user__id=pk)
            userprojectdata=User_projectSerializer(userproject,many=True)
            return JsonResponse(
                    {
                        'status':200,
                        'data':userprojectdata.data
                        
                    }
                )
        
        userproject=user_project.objects.all()
        userprojectdata=User_projectSerializer(userproject,many=True)
        return JsonResponse(
                    {
                        'status':200,
                        'data':userprojectdata.data
                        
                    }
                )

    def post(self,request):
        data=request.data
    
        try:
            serializer=User_projectSerializer(data=data)
            if not serializer.is_valid():
                print(serializer.errors)
                return JsonResponse(
                    {
                        'status':403,
                        'errors':serializer.errors
                        
                    }
                )
            resp=serializer.save()
            return JsonResponse(
                    {
                        'status':200, 
                        'msg':'Your project detail is saved'
                     }
                )
        except Exception as e : 
            return JsonResponse(
                {
                    'status':404,
                    'error':'something went wrong'
                }
            )
    

    def delete(self, request,pk):
        print(pk)   
        userproject=user_project.objects.get(id=pk)
        userproject.delete()
        return JsonResponse(
                    {
                        'status':200,
                        'data':' your project detail is deleted'
                        
                    }
                )

    def put(self, request, pk, format=None):
        prof_detail = user_project.objects.get(id=pk)
        try:
            serializer = User_projectSerializer(prof_detail, data=request.data)

        except Exception as e:  
            print(e)
            pass
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status':True,'updated_skill':serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                 