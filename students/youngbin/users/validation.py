import re
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

REGEX_PASSWORD = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
REGEX_EMAIL = r'^\w+[\.\w]*@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$'
REGEX_PHONE_NUMBER = r'^\d{3}-\d{3,4}-\d{4}$'

def validate_password(password):
    if not re.search(REGEX_PASSWORD,password):
        raise ValidationError('INVALID_PASSWORD')
    return password

def validate_email(email):
    if not re.search(REGEX_EMAIL,email):
        raise ValidationError('INVALID_EMAIL_ADDRESS')
    return email

def validate_phone_number(phone_number):
    if not re.search(REGEX_PHONE_NUMBER,phone_number):
        raise ValidationError('INVALID_PHONE_NUMBER')
    return phone_number