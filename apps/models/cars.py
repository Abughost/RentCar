from django.db.models import CharField, IntegerField, ImageField, ForeignKey, CASCADE, ManyToManyField, TextChoices

from apps.models.base import UUIDBaseModel, CreatedBaseModel


class CarType(UUIDBaseModel):
    name = CharField(max_length=50)


class CarBrand(UUIDBaseModel):
    name = CharField(max_length=50)
    logo = ImageField(upload_to='car/brand/logo/%Y/%m/%d/')


class Car(CreatedBaseModel):
    class FuelType(TextChoices):
        GAS = 'gas', 'Gas'
        ELECTRIC = 'electric', 'Electric'
        HYBRID = 'hybrid', 'Hybrid'

    class TransmissionType(TextChoices):
        MANUAL = 'manual', 'Manual',
        AUTOMATIC = 'automatic', 'Automatic'

    model = CharField(max_length=100)
    brand = ForeignKey('CarBrand', CASCADE, related_name='car_brand')
    type = ForeignKey('CarType', CASCADE, related_name='car_type')
    color = CharField(max_length=50)  # TODO fk qilish kk
    deposit = IntegerField()
    limit_km = IntegerField()
    daily_price = IntegerField()
    fuel_type = CharField(max_length=15, choices=FuelType.choices, default=FuelType.GAS)
    transmission_type = CharField(max_length=15, choices=TransmissionType.choices, default=TransmissionType.AUTOMATIC)
    features = ManyToManyField('apps.Feature', through='apps.CarFeature')


class CarImage(UUIDBaseModel):
    car = ForeignKey('Car', CASCADE, related_name='images')
    image = ImageField(upload_to='car/images/%Y/%m/%d/')


class CarFeature(UUIDBaseModel):
    car = ForeignKey('Car', CASCADE)
    feature = ForeignKey('Feature', CASCADE)


class Feature(UUIDBaseModel):
    icon = ImageField()
    name = CharField(max_length=155)
    description = CharField(max_length=155)
