from rest_framework.fields import SerializerMethodField, HiddenField, CurrentUserDefault
from rest_framework.serializers import CharField, ModelSerializer

from apps.models import Car, CarBrand, CarCategory, CarImage, CarPrice, Feature


class CarPriceModelSerializer(ModelSerializer):
    class Meta:
        model = CarPrice
        exclude = ('id', 'car', 'created_at', 'updated_at',)


class CarFeatureModelSerializer(ModelSerializer):
    class Meta:
        model = Feature
        fields = 'name', 'description', 'icon'


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
        fields = 'image',


class CarModelSerializer(ModelSerializer):
    daily_price = SerializerMethodField()
    features = CarFeatureModelSerializer(many=True)
    author = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Car
        fields = 'id', "model", 'daily_price', 'deposit', 'limit_km', 'features'

    def get_daily_price(self, obj) -> int:
        price = CarPrice.objects.filter(car=obj.id).first()
        return price.daily_price if price else None


class CarDetailModelSerializer(ModelSerializer):
    brand = CharField(source='brand.name')
    prices = CarPriceModelSerializer(many=True, source='price')
    features = CarFeatureModelSerializer(many=True)
    images = CarImageModelSerializer(many=True)
    similar_cars = SerializerMethodField()
    author = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Car
        fields = 'id', 'model', 'brand', 'prices', 'features', 'similar_cars', 'images'
        lookup_fields = 'id', 'model'

    def get_similar_cars(self, obj):
        similar = Car.objects.filter(category=obj.category).exclude(id=obj.id)[:4]
        return CarModelSerializer(similar, many=True).data
