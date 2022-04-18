import json
from django.core.exceptions import ValidationError
from django.http            import JsonResponse
from django.views           import View
from .models                import User
from .validation            import (
    validate_password,
    validate_email,
    validate_phone_number)

class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body) 

        try:
            new_email        = data['email']
            new_password     = data['password']
            new_name         = data['name']
            new_phone_number = data['phone_number']

            validated_password = validate_password(new_password)
            validated_email = validate_email(new_email)
            validated_phone_number = validate_phone_number(new_phone_number)
        
            if User.objects.filter(email=new_email).exists():
                return JsonResponse({"message":"ALREADY_EXISTED_EMAIL"},status=409)

            User.objects.create(
                name         = new_name,
                password     = validated_password,
                email        = validated_email,
                phone_number = validated_phone_number,
            )
            return JsonResponse({'messasge':'created'}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except ValidationError as error:
            return JsonResponse({"message": error.messages}, status=409)


