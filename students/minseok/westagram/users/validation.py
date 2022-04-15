from django.http  import JsonResponse, HttpResponse
import re
from users.models import User

class Validate:
      def validate(value):
          Regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
          Regex_password = '\S{8,25}'
          if not re.match(Regex_email, str(User.email)):
             return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
          if not re.match(Regex_password, str(User.password)):
             return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
                