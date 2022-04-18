from django.shortcuts import render

# Create your views here.

import json, re

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from my_settings      import SECRET_KEY
from users.models     import User
from users.validation import Validation

class SignUpView(View):
      def post(self, request):
          try:
              data         = json.loads(request.body)
              email        = data['email']
              password     = data['password']
              name         = data['name']
              phone_number = data['phone_number']

              Validation.email_validate(email)
              Validation.password_validate(password)

              if User.objects.filter(email=email).exists():
                  return JsonResponse({'message': 'ALREADY_EXISTS'}, status = 400)
                      
              User.objects.create(
                  name = name,
                  email = email, 
                  password = password, 
                  phone_number = phone_number
                  )
              return JsonResponse({'message': 'SUCCESS'}, status = 201)

          except KeyError:
              return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
