import json, re, bcrypt, jwt

from django.shortcuts   import render
from django.http        import JsonResponse
from django.views       import View
from users.models       import User
from westagram.settings import SECRET_CODE, ALGORITHM

REGEX_EMAIL    = r'^[a-zA-Z0-9+-_.]+@[a-zA-z0-9-]+\.[a-zA-z0-9-]+$'
REGEX_PASSWORD = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
SECRET_CODE    = SECRET_CODE
ALGORITHM      = ALGORITHM

def check_email_validation(email):
    return re.match(REGEX_EMAIL, email)
        
def check_password_validation(password):
    return re.match(REGEX_PASSWORD, password)

class RegisterView(View):
    def post(self, request):
        try : 
            data             = json.loads(request.body)
            entered_email    = data['email']
            entered_password = data['password']
            hashed_password  = bcrypt.hashpw(entered_password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")

            if check_email_validation(entered_email) == None:
                return JsonResponse({'MESSAGE' : "Email validation error"},    status = 400)

            if check_password_validation(entered_password) == None:
                return JsonResponse({'MESSAGE' : "Password validation error"}, status = 400)
                
            if User.objects.filter(email = entered_email ).exists():
                return JsonResponse({'MESSAGE' : 'Email already Exists'},      status = 400)
        
            User.objects.create(
                name         = data['name'],
                email        = entered_email,
                password     = hashed_password,
                phone_number = data['phone_number'],
            )
            return JsonResponse({'MESSAGE' : 'SUCCESS'},                       status = 201)

        except KeyError :
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'},                     status = 400)
            
class LoginView(View):
    def post(self, request):
        try: 
            data             = json.loads(request.body)
            entered_email    = data['email']
            entered_password = data['password']
            secret_code      = str(SECRET_CODE)
            algorithms       = str(ALGORITHM)
            
            if not User.objects.filter(email=entered_email).exists(): 
                return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status = 401)

            user_db          = User.objects.filter(email=entered_email)[0]
            db_password      = user_db.password.encode('utf-8')

            if not bcrypt.checkpw(entered_password.encode('utf-8'), db_password): 
                return JsonResponse({'MESSAGE' : 'INVALID_PW'}, status = 401)

            jwt_token        = jwt.encode({'id' : user_db.id}, secret_code, algorithm = algorithms)
            return JsonResponse({'MESSAGE'     : 'LOGIN SUCCESS' , 'JWT_TOKEN' : jwt_token}, status = 200)

        except KeyError: 
            return JsonResponse({'MESSAGE'     : 'KEY_ERROR'}, status = 400)