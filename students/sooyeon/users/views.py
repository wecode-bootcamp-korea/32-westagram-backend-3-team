from django.shortcuts import render

from django.conf import settings
from django.http import JsonResponse
from django.views import View
from users.models import User
from .validation import *
import json, bcrypt, jwt

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
            
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
            User.objects.create(
                name     = data['name'],
                email    = data['email'],
                password = hashed_password,
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
            email = data['email']
            
            user = User.objects.get(email=email)

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=401)

            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
            
            return JsonResponse({
                 "message"      : "SUCCESS",
                 "access_token" : access_token
            }, status=200)
            
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_EMAIL"}, status=401)