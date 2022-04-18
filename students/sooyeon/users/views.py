from django.shortcuts import render

import json

from django.http import JsonResponse
from django.views import View

from users.models import User
import re

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            name     = data['name']
            email    = data['email']
            password = data['password']
            contact  = data['contact']
        
            EMAIL_REGEX = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
            PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[$@$!%*#?&])[A-Za-z0-9$@$!%*#?&].{8,}$"
        
            if re.match(EMAIL_REGEX, email) is None:
                return JsonResponse({'message': 'EMAIL_INVALIDATION'}, status = 400)
        
            if re.match(PASSWORD_REGEX, password) is None:
                return JsonResponse({'message': 'PASSWORD_INVALIDATION'}, status = 400)
    
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'EMAIL_ALREADY_EXISTS'}, status = 400)
        
            User.objects.create(
                name     = data['name'],
                email    = data['email'],
                password = data['password'],
                contact  = data['contact']
            )
        
            return JsonResponse({'message':'SUCCESS'}, status = 201)
        
        except:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        
        