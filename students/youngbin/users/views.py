import json
from django.http import JsonResponse
from .models import User
from django.views import View
import re

#Q : 비밀번호나 이메일이 틀렸을 경우 반환 statuscode를 뭘로 해야하나요? 401(unauthorized)? 403(forbidden)?
#A : 모르겠으면 그냥 400때리라고 함;;

#Q :에러케이스를 잡다보니까 에러들간의 위계가 발생하는데 위계를 설정하는 기준이 있는지?
#A : 일단은 특별한 기준은 없는 듯함
#Passwordvalidation > 있는지 없는지만 체크 > re.search
def passwordValidation(password):
    if len(password) < 8:
        return JsonResponse({"message":"Incorrect password format : too short"},status=401)
    elif re.search('[0-9]+',password) is None:
        return JsonResponse({"message":"Incorrect password format : no numbers"},status=401)
    elif re.search('[a-zA-Z]+',password) is None:
        return JsonResponse({"message":"Incorrect password format : no letters"},status=401)
    elif re.search('[`~!@#$%^&*(),<.>]+',password) is None:
        return JsonResponse({"message":"Incorrect password format : need special letters"},status=401)
    else:
        return password


#Q: re.search가 아니라 re.fullmatch를 써야 하나요?
#A
# search는 있는지 없는지만 검색하는 거라, 의미적으로는 fullmatch가 맞다
# 근데 정규표현식에서 ^와 $를 사용시 반드시 ^뒤의 문자로 시작해서 $로 끝이 나야하므로 re.search를 써도 됨. 반대로 ^와 $를 사용하지 않을거라면 re.fullmatch를 반드시 사용해야 한다.

def emailValidation(email):
    if re.search('^\w+[\.\w]*@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$',email) is None:
        return JsonResponse({"message":"Incorrect email format"},status=400)
    else:
        return email


class Userview(View):
    def post(self,request):
        data = json.loads(request.body) 

        #KeyError check
        try:
            new_email = data['email']
            new_password = data['password']
            new_name=data['name']
            new_phone_number=data['phone_number']
        except:
            return JsonResponse({"message":"KEY_ERROR"},status=400)

        #Q : 유효성 검사가 틀렸는데 왜 user가 생성이 되냐..
        #A : isinstance로 로직을 확인해서 리턴해주지 않으면 Jsonresponse자체가 db에 들어감.
        validated_pw = passwordValidation(new_password)
        if isinstance(validated_pw,JsonResponse):
            return validated_pw
        
        #이메일 유효성 검사
        validated_email = emailValidation(new_email)
        if isinstance(validated_email,JsonResponse):
            return validated_email
        

        #email 중복 검증
        #의문점 : model에 unique옵션이 있으니까 save했다가 에러가 나는 걸로 중복체크를 할 수 있지 않을까? 코드가 훨씬 간단해질 듯?
        user_group = User.objects.all()
        email_list = []
        for user in user_group:
            email_list.append(user.email)
        if new_email in email_list:
            return JsonResponse({"message":"ALREADY_EXISTED_EMAIL"},status=409)
            #409 코드는 리소스의 현재 상태와 충돌해서 해당 요청을 처리할 수 없어 클라이언트가 충돌을 수정해서 다시 요청을 보내야할 때 사용된다.

        #user계정생성
        User.objects.create(
            name = new_name,
            password = validated_pw,
            email = validated_email,
            phone_number = new_phone_number,
        )
        return JsonResponse({'messasge':'created'}, status=201)

    
