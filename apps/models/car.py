from django.db.models import ImageField, ForeignKey, CASCADE
from django.db.models.fields import CharField, IntegerField

from apps.models.base import CustomUuidModel, CustomDataCreationModel


class CarType(CustomUuidModel):
    name = CharField(max_length=50)


class Car(CustomUuidModel,CustomDataCreationModel):
    model = CharField(max_length=100)
    brand_name = CharField(max_length=50)
    brand_image = ImageField()
    color = CharField(max_length=50)
    deposit = IntegerField()
    limit_km = IntegerField()
    daily_price = IntegerField()


class CarImage(CustomUuidModel):
    car = ForeignKey('Car',on_delete=CASCADE,related_name='car_image')
    image = ImageField(upload_to='car/%Y/%m/%d/')


class CarFeature(CustomUuidModel):
    car = ForeignKey('Car',on_delete=CASCADE,related_name='car_feature')
    feature = ForeignKey('Feature', on_delete=CASCADE, related_name='feature')


class Feature(CustomUuidModel):
    icon = ImageField()
    feature = CharField(max_length=15)
    description = CharField(max_length=50)

