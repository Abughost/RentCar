import re
from random import randint

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from redis import Redis
from rest_framework import status
from rest_framework.exceptions import ValidationError

from root.settings import EMAIL_HOST_USER


def get_login_data(value):
    return f"login:{value}"

def send_code(data, expired_time=360):
    redis = Redis.from_url(settings.CACHES['default']['LOCATION'])
    _contact = get_login_data(data['value'])
    _ttl = redis.ttl(f':1:{_contact}')
    code = randint(100_000,999_999)

    if _ttl > 0:
        return False, _ttl

    print('send code start ')
    if data['type'] == 'email':
        print('email sending')
        send_email(data['value'],code)
    else:
        print(f'{data['type']}: {data['value']} == Code: {code}')

    _data = {
        'code':code,
        'type':data['type'],
        'first_name':data['first_name'],
        'last_name':data['last_name'],
        'password':data['password']
    }
    cache.set(_contact, _data, expired_time)
    return True, 0

def check_contact(contact: str, code: int):
    _contact = get_login_data(contact['value'])
    _data = cache.get(f"{_contact}")
    if _data is None:
        raise ValidationError('Invalid email or phone number', status.HTTP_404_NOT_FOUND)
    return _data['code'] == code , _data

def normalize_phone(value):
    digits = re.findall(r'\d', value)
    if len(digits) < 9:
        raise ValidationError('Phone number must be at least 9 digits')
    phone = ''.join(digits)
    if len(phone) > 9 and phone.startswith('998'):
        phone = phone.removeprefix('998')
    return phone

def find_contact_type(contact):
    try:
        validate_email(contact)
        return {'type': 'email', 'value': contact}
    except DjangoValidationError:
        pass

    try:
        normalize_phone(contact)
        return {'type': 'phone', 'value': contact}
    except ValidationError:
        pass

    raise ValidationError({'message': 'contact must be phone number or email'})

def send_email(email:str, code:int):
    subject = 'Hello world'
    message = f'please confirm the code {code}'
    send_mail(subject,message,EMAIL_HOST_USER,[email])
