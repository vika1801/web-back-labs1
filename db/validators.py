import re

def validate_login(login):
    return bool(re.match(r'^[a-zA-Z0-9._-]+$', login) and 3 <= len(login) <= 30)

def validate_password(password):
    return bool(re.match(r'^[a-zA-Z0-9!@#$%^&*._-]+$', password) and len(password) >= 6)

def validate_phone(phone):
    return bool(re.match(r'^\+?[1-9]\d{1,14}$', phone))

def validate_amount(amount):
    return amount > 0