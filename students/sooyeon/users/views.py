from xml.dom import ValidationErr
from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from users.models import User
from .validation import *

import json

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            name     = data['name']
            email    = data['email']
            password = data['password']
            contact  = data['contact']
            
            signup_email(email)
            signup_password(password)
    
            if User.objects.filter(email = email).exists():
                return JsonResponse({'message':'EMAIL_ALREADY_EXISTS'}, status = 400)
        
            User.objects.create(
                name     = data['name'],
                email    = data['email'],
                password = data['password'],
                contact  = data['contact']
            )
        
            return JsonResponse({'message':'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        
        except ValidationError as e:
            return JsonResponse({"message" : e.message}, status = 400)
        

class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email    = data['email']
            password = data['password']
            
            if not User.objects.filter(email = email, password = password).exists():
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
            
            else:
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)
  
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)