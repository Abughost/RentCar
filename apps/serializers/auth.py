from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import User
from apps.serializers.user import UserModelSerializer
from apps.utils import check_contact, find_contact_type, normalize_phone


class SendCodeSerializer(Serializer):
    contact = CharField(
        help_text="User email or phone number for verification",
        label="Email or Phone",
        default='901001010')

    first_name = CharField(max_length=255, default='Alijon')
    last_name = CharField(max_length=255, default='Valiyev')
    password = PasswordField(max_length=255)

    def validate_contact(self, contact):
        contact_data = find_contact_type(contact)
        user = User.objects.filter(contact=contact_data['value'])
        if user:
            raise ValidationError({'message': 'user already exist'})
        return contact_data


class VerifyCodeSerializer(Serializer):
    contact = CharField(help_text="User email or phone number for verification",
                        label="Email or Phone",
                        default='901001010')
    code = IntegerField()

    def validate_contact(self, contact):
        try:
            validate_email(contact)
            return {'type': 'email', 'value': contact}
        except DjangoValidationError:
            pass

        return {'type': 'phone', 'value': normalize_phone(contact)}

    def validate(self, attrs: dict[str, Any]) -> dict[Any, Any]:
        is_valid, data = check_contact(**attrs)
        if not is_valid:
            raise ValidationError({'message': 'invalid or expired code'})

        user, _ = User.objects.get_or_create(
            contact=attrs['contact']['value'],
            defaults={
                  'first_name' : data['first_name'],
                  'last_name' : data['last_name'],
                  'password' : make_password(data['password'])
                    }
        )

        attrs['user'] = UserModelSerializer(user).data
        return attrs


class LoginSerializer(Serializer):
    contact = CharField(max_length=255, default='901001010')
    password = CharField(max_length=50)
    token_class = RefreshToken
    user = None

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def validate_contact(self, contact):
        return find_contact_type(contact)

    def validate(self, attrs):
        contact = attrs['contact']['value']
        password = attrs['password']

        try:
            self.user = User.objects.get(contact=contact)
        except User.DoesNotExist:
            return ValidationError(self.default_error_messages)

        if not self.user.check_password(password):
            raise ValidationError({"datail" : 'Incorrect password'})
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
            "data" : {**tokens, **user_data}
        }
        return data

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)
