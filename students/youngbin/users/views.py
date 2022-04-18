import json

from django.http  import JsonResponse
from django.views import View
from .models      import User
from .validation  import (
    validate_password,
    validate_email,
    validate_phone_number)

class UserView(View):
    def post(self,request):
        data = json.loads(request.body) 

        try:
            new_email        = data['email']
            new_password     = data['password']
            new_name         = data['name']
            new_phone_number = data['phone_number']


            validated_pw = validate_password(new_password)
            if isinstance(validated_pw,JsonResponse):
                return validated_pw
            
            validated_email = validate_email(new_email)
            if isinstance(validated_email,JsonResponse):
                return validated_email

            validated_phone_number = validate_phone_number(new_phone_number)
            if isinstance(validated_phone_number,JsonResponse):
                return validated_phone_number
            

            if User.objects.filter(email=new_email).exists():
                return JsonResponse({"message":"ALREADY_EXISTED_EMAIL"},status=409)

            User.objects.create(
                name         = new_name,
                password     = validated_pw,
                email        = validated_email,
                phone_number = validated_phone_number,
            )
            return JsonResponse({'messasge':'created'}, status=201)

        except:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
