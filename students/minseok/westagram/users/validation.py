from django.http  import JsonResponse, HttpResponse
import re
from users.models import User

class Validate:
      def validate(value):
          REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
          REGEX_PASSWORD = '\S{8,25}'
          if not re.match(REGEX_EMAIL, 'email'):
             return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
          if not re.match(REGEX_PASSWORD, 'password'):
             return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
                
