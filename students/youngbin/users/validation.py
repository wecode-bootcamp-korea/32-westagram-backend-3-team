import re
from django.http import JsonResponse


def validate_password(password):
    REGEX_PASSWORD = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
    if re.search(REGEX_PASSWORD,password) is None:
        return JsonResponse({"message":"Incorrect password format"},status=401)
    return password

def validate_email(email):
    REGEX_EMAIL = r'^\w+[\.\w]*@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$'
    if re.search(REGEX_EMAIL,email) is None:
        return JsonResponse({"message":"Incorrect email format"},status=400)
    return email

def validate_phone_number(phone_number):
    REGEX_PHONE_NUMBER = r'^\d{3}-\d{3,4}-\d{4}$'
    if re.search(REGEX_PHONE_NUMBER,phone_number) is None:
        return JsonResponse({"message":"Incorrect phone_number format"},status=409)
    return phone_number