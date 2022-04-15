import re
from django.http import JsonResponse

def password_validation(password):
    if len(password) < 8:
        return JsonResponse({"message":"Incorrect password format : too short"},status=401)
    elif re.search('[0-9]+',password) is None:
        return JsonResponse({"message":"Incorrect password format : no numbers"},status=401)
    elif re.search('[a-zA-Z]+',password) is None:
        return JsonResponse({"message":"Incorrect password format : no letters"},status=401)
    elif re.search('[`~!@#$%^&*(),<.>]+',password) is None:
        return JsonResponse({"message":"Incorrect password format : need special letters"},status=401)
    else:
        return password

def email_validation(email):
    regex = '^\w+[\.\w]*@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$'
    if re.search(regex,email) is None:
        return JsonResponse({"message":"Incorrect email format"},status=400)
    return email