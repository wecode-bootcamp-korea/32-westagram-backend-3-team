import json
import re

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from users.models import User

def check_email_validation(email):
    regex = r'^[a-zA-Z0-9+-_.]+@[a-zA-z0-9-]+\.[a-zA-z0-9-]+$'
    if re.match(regex, email):
        return True
    else :
        return False

def check_password_validation(password):
    regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
    if re.match(regex, password):
        return True
    else :
        return False


class JoinView(View):
    def post(self, request):
        data = json.loads(request.body)
        data_keys = list(data.keys())

        if 'email' not in data_keys or 'password' not in data_keys:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        elif not check_email_validation(data['email']):
            return JsonResponse({'MESSAGE' : "Email validation error"}, status=400)

        elif not check_password_validation(data['password']):
            return JsonResponse({'MESSAGE' : "Password validation error"}, status=400)

        elif User.objects.filter(email = data["email"]).exists():
            return JsonResponse({'MESSAGE' : 'Email already Exists'},status=400)

        else:
            User.objects.create(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                phone_number=data['phone_number'],
            )
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
