import json
import re

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from users.models import User

REGEX_EMAIL = r'^[a-zA-Z0-9+-_.]+@[a-zA-z0-9-]+\.[a-zA-z0-9-]+$'
REGEX_PASSWORD = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

def check_email_validation(email):
    return re.match(REGEX_EMAIL, email)
        
def check_password_validation(password):
    return re.match(REGEX_PASSWORD, password)

class RegisterView(View):
    def post(self, request):
        try : 
            data = json.loads(request.body)
            if check_email_validation(data['email']) == None:
                return JsonResponse({'MESSAGE' : "Email validation error"},    status = 400)

            if check_password_validation(data['password']) == None:
                return JsonResponse({'MESSAGE' : "Password validation error"}, status = 400)

            if User.objects.filter(email = data["email"]).exists():
                return JsonResponse({'MESSAGE' : 'Email already Exists'},      status = 400)
            
            User.objects.create(
                name =         data['name'],
                email =        data['email'],
                password =     data['password'],
                phone_number = data['phone_number'],
            )
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

class LoginView(View):
    def get(self, request):
        try: 
            data = json.loads(request.body)
            entered_password = ''

            if not User.objects.filter(email=data['email']).exists(): #이메일존재여부
                return JsonResponse({'MESSAGE' : 'EMAIL NOT EXIST'}, status = 401)
            else: 
                entered_password = data['password']
                real_password = User.objects.get(email=data['email']).password                

            if not entered_password == real_password: #비번일치여부_일치하면 로그인 성공
                return JsonResponse({'MESSAGE' : 'PASSWORD ERROR'}, status = 401)
            else:
                return JsonResponse({'MESSAGE' : 'LOGIN SUCCESS'}, status = 200)

        except KeyError: 
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)