from django.shortcuts import render

# Create your views here.

import json, re, bcrypt, jwt

from django.http import JsonResponse, HttpResponse
from django.views import View
from my_settings    import SECRET_KEY
from users.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']
            name = data['name']
            phone_number = data['phone_number']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'ALREADY_EXISTS'}, status = 400)

            regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
            regex_password = '\S{8,25}'
            if not re.match(regex_email, email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
            if not re.match(regex_password, password):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
                
            password       = data['password'].encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
        
            User.objects.create(name = name, email = email, password = password_crypt, phone_number = phone_number)
            return JsonResponse({'message': 'SUCCESS'}, status = 201)


        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)


        


