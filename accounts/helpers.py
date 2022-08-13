from distutils.log import error
import random
from django.core.cache import cache
from django.http import JsonResponse

import urllib.request
import urllib.parse

humhaiAPIKey = 'NTk2NzY3NzM3MTU1Njg0ZTU3NWE3NDY3NmE3OTZkNWE='

def sendSMS(numbers, message):
 
    data = urllib.parse.urlencode({'apikey': humhaiAPIKey, 'numbers': numbers,
                             'message': message, 'sender': 'HUMHAI'})
 
    data = data.encode('utf-8')

    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
  
    return(fr)






def send_otp_mobile(mobile, user_obj):
    if cache.get(mobile):
        return False ,cache.ttl(mobile)
    try:
        otp_to_sent=random.randint(1000,9999)
        cache.set(mobile,otp_to_sent ,timeout=60)
        user_obj.otp=otp_to_sent
        user_obj.save()
        otp=  str(otp_to_sent)
        print(mobile)
        print(otp)  
        first_name='dear'  
        resp = sendSMS(mobile, 'Hello '+first_name+',\nYour OTP for HUMHAI Login is ' + otp +
                           ',\nUse this OTP for Logging into HUMHAI.IN\n\nThanks & Regards,\nTeam HUMHAI.IN')
        print(resp,43)                   
        return True, 0

    except Exception as e:
        print(e)

    return JsonResponse({'error': 'try after some time'})    

        