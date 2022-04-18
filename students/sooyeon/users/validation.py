from django.core.exceptions import ValidationError
import re

def signup_email(email):
    EMAIL_REGEX = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if re.match(EMAIL_REGEX, email) is None:
        raise ValidationError("EMAIL_INVALIDATION")
                           
def signup_password(password):
    PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[$@$!%*#?&])[A-Za-z0-9$@$!%*#?&].{8,}$"
    if re.match(PASSWORD_REGEX, password) is None:
        raise ValidationError("PASSWORD_INVALIDATION")
                