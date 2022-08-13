import email
from rest_framework import serializers
from .helpers import send_otp_mobile  
from .models import *

class   UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','password','phone','first_name','last_name','gender']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user=User.objects.create(email=validated_data['email'], phone=validated_data['phone'],first_name=validated_data['first_name'], last_name=validated_data['last_name'], gender=validated_data['gender'],)
        user.set_password(validated_data['password'])
        user.save()
        send_otp_mobile(user.phone,user)
        return user