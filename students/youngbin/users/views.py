import json

from django.http import JsonResponse
from django.views import View
from .models import User
from .validation import password_validation,email_validation


class UserView(View):
    def post(self,request):
        data = json.loads(request.body) 

        #KeyError check
        try:
            new_email = data['email']
            new_password = data['password']
            new_name=data['name']
            new_phone_number=data['phone_number']

            validated_pw = password_validation(new_password)
            if isinstance(validated_pw,JsonResponse):
                return validated_pw
            
            validated_email = email_validation(new_email)
            if isinstance(validated_email,JsonResponse):
                return validated_email
            

            user_group = User.objects.all()
            email_list = []
            for user in user_group:
                email_list.append(user.email)
            if new_email in email_list:
                return JsonResponse({"message":"ALREADY_EXISTED_EMAIL"},status=409)

            User.objects.create(
                name = new_name,
                password = validated_pw,
                email = validated_email,
                phone_number = new_phone_number,
            )
            return JsonResponse({'messasge':'created'}, status=201)

        except:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
