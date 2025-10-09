from django.db.models import (CASCADE, ForeignKey, ImageField, ManyToManyField,
                              TextChoices)
from django.db.models.fields import CharField, IntegerField

from apps.models.base import CreatedBaseModel, UUIDBaseModel


class FuelType(TextChoices):
    GAS = 'gas', 'Gas'
    ELECTRIC = 'electric', 'Electric'
    HYBRID = 'hybrid', 'Hybrid'


class TransmissionType(TextChoices):
    MANUAL = 'manual', 'Manual',
    AUTOMATIC = 'automatic', 'Automatic'


class CarType(UUIDBaseModel):
    name = CharField(max_length=50)


class CarBrand(UUIDBaseModel):
    name = CharField(max_length=50)
    logo = ImageField(upload_to='car/brand/logo/%Y/%m/%d/')


class Car(UUIDBaseModel, CreatedBaseModel):
    model = CharField(max_length=100)
    brand = ForeignKey('CarBrand', on_delete=CASCADE, related_name='car_brand')
    type = ForeignKey('CarType', on_delete=CASCADE, related_name='car_type')
    color = CharField(max_length=50)
    deposit = IntegerField()
    limit_km = IntegerField()
    daily_price = IntegerField()
    fuel_type = CharField(max_length=15, choices=FuelType.choices, default=FuelType.GAS)
    transmission = CharField(max_length=15, choices=TransmissionType.choices, default=TransmissionType.AUTOMATIC)


class CarImage(UUIDBaseModel):
    car = ForeignKey('Car', on_delete=CASCADE, related_name='car_image')
    image = ImageField(upload_to='car/%Y/%m/%d/')

class CarFeature(UUIDBaseModel):
    car = ForeignKey('Car', on_delete=CASCADE)
    feature = ForeignKey('Feature', on_delete=CASCADE)


class Feature(UUIDBaseModel):
    icon = ImageField()
    name = CharField(max_length=15)
    description = CharField(max_length=50)
