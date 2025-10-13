import re
from typing import Any

from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import User, CarBrand
from apps.models.cars import Car
from apps.utils import check_phone


class CarModelSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = 'id','model','brand','color'

class CarBrandSerializer(ModelSerializer):
    class Meta:
        model = CarBrand
        fields = 'name',



class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id','phone'

class SendCodeSerializer(Serializer):
    phone = CharField(default='901001010')

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9 :
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        if len(phone) > 9 and phone.startswith('998'):
            phone = phone.removeprefix('998')
        return phone

class VerifyCodeSerializer(Serializer):
    phone = CharField(default='901001010')
    code = IntegerField()
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9 :
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        if len(phone) > 9 and phone.startswith('998'):
            phone = phone.removeprefix('998')
        return phone

    def get_data(self):
        refresh = self.get_token(self.user)
        user_data = UserModelSerializer(self.user).data

        tokens = {
            'access token' : str(refresh.access_token),
            'refresh token' : str(refresh)
        }
        data = {
            'message':'Valid Code',
            **tokens,**user_data
        }
        return data

    def validate(self, attrs: dict[str, Any]) -> dict[Any, Any]:
        is_valid = check_phone(**attrs)
        if not is_valid:
            raise ValidationError({'message': 'invalid or expired code'})
        phone = attrs['phone']

        self.user , _ = User.objects.get_or_create(phone=phone)
        attrs['user'] = self.user
        return attrs



    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)  # type: ignore




