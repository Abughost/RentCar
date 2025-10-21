import re
from typing import Any

from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer, CharField
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import User, CarBrand, CarCategory, Car, CarPrice, Feature, CarImage, Rental
from apps.models.users import UserProfile
from apps.utils import check_phone
from root.settings import LANGUAGE_CODE


class CarModelSerializer(ModelSerializer):
    daily_price = SerializerMethodField()

    class Meta:
        model = Car
        fields = "__all__"


    def get_daily_price(self,obj):
        price = CarPrice.objects.filter(car=obj.id).first()
        return price.daily_price if price else None

class CarPriceModelSerializer(ModelSerializer):
    class Meta:
        model = CarPrice
        exclude = ('id','car','created_at','updated_at',)

class CarFeatureModelSerializer(ModelSerializer):
    class Meta:
        model = Feature
        fields = 'name','description','icon'

class CarBrandModelSerializer(ModelSerializer):
    class Meta:
        model = CarBrand
        fields = 'id', 'name', 'logo'

class CarCategoryModelSerializer(ModelSerializer):
    class Meta:
        model = CarCategory
        fields = 'id', 'name'

class CarImageModelSerializer(ModelSerializer):
    class Meta:
        model = CarImage
        fields ='image',

class CarDetailModelSerializer(ModelSerializer):
    brand = CharField(source='brand.name')
    prices = CarPriceModelSerializer(many=True, source='price')
    features = CarFeatureModelSerializer(many=True)
    images = CarImageModelSerializer(many=True)
    similar_cars = SerializerMethodField()


    class Meta:
        model = Car
        fields = 'id', 'model', 'brand','prices','features','similar_cars','main_photo','images'
        lookup_fields = 'id','model'

    def get_similar_cars(self, obj):
        similar = Car.objects.filter(category=obj.category).exclude(id=obj.id)[:4]
        return CarModelSerializer(similar, many=True).data

class VerifiedUserModelSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = 'user',

class RentModelSerializer(ModelSerializer):
    class Meta:
        model = Rental
        exclude = 'user',


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'phone'

class SendCodeSerializer(Serializer):
    phone = CharField(default='901001010')

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
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
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        if len(phone) > 9 and phone.startswith('998'):
            phone = phone.removeprefix('998')
        return phone

    def get_data(self):
        refresh = self.get_token(self.user)
        user_data = UserModelSerializer(self.user).data

        tokens = {
            'access token': str(refresh.access_token),
            'refresh token': str(refresh)
        }
        data = {
            'message': 'Valid Code',
            **tokens, **user_data
        }
        return data

    def validate(self, attrs: dict[str, Any]) -> dict[Any, Any]:
        is_valid = check_phone(**attrs)
        if not is_valid:
            raise ValidationError({'message': 'invalid or expired code'})
        phone = attrs['phone']

        self.user, _ = User.objects.get_or_create(phone=phone)
        attrs['user'] = self.user
        return attrs

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)  # type: ignore
