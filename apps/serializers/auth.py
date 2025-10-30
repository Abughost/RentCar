from typing import Any

from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import User
from apps.serializers import UserModelSerializer
from apps.utils import normalize_phone, check_phone


class SendCodeSerializer(Serializer):
    phone = CharField(default='901001010')
    first_name = CharField(max_length=255,default='Alijon')
    last_name = CharField(max_length=255,default='Valiyev')
    password = PasswordField(max_length=255)

    def validate_phone(self, value):
        normalize_phone(value)

class VerifyCodeSerializer(Serializer):
    phone = CharField(default='901001010')
    code = IntegerField()

    def validate_phone(self, value):
        return normalize_phone(value)

    def validate(self, attrs: dict[str, Any]) -> dict[Any, Any]:
        is_valid, data = check_phone(**attrs)
        if not is_valid:
            raise ValidationError({'message': 'invalid or expired code'})
        phone = attrs['phone']
        user, _ = User.objects.get_or_create(phone=phone,
                                                  first_name=data['first_name'],
                                                  last_name=data['last_name'],
                                                  password=make_password(data['password']))

        attrs['user'] = UserModelSerializer(user).data
        return attrs

class LoginSerializer(Serializer):
    phone = CharField(max_length=255,default='901001010')
    password = CharField(max_length=50)
    token_class = RefreshToken
    user = None


    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def validate_phone(self,value):
        return normalize_phone(value)

    def validate(self, attrs):
        phone = attrs['phone']
        password = attrs['password']

        try:
            self.user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return ValidationError(self.default_error_messages)

        if not self.user.check_password(password):
            raise ValidationError({"datail":'Incorrect password'})
        return attrs

    def get_data(self):
        refresh = self.get_token(self.user)
        user_data = UserModelSerializer(self.user).data

        tokens = {
            'access token': str(refresh.access_token),
            'refresh token': str(refresh)
        }
        data = {
            'message': 'Valid Code',
            "data":{**tokens, **user_data}
        }
        return data

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)  # type: ignore
