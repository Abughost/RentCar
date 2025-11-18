from django.db.models import (CASCADE, BooleanField, CharField, DateField,
                              ForeignKey, ImageField, IntegerField,
                              ManyToManyField, TextChoices)
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import CreatedBaseModel, UUIDBaseModel


class CarCategory(UUIDBaseModel):
    name = CharField(max_length=50)

    def __str__(self):
        return self.name


class CarBrand(UUIDBaseModel):
    name = CharField(max_length=50)
    logo = ImageField(upload_to='car/icons/brand_logo/%Y/%m/%d/')

    def __str__(self):
        return self.name


class CarColor(UUIDBaseModel):
    name = CharField(max_length=155)

    def __str__(self):
        return self.name


class CarPrice(CreatedBaseModel):
    car = ForeignKey('apps.Car', CASCADE, related_name='price')
    daily_price = IntegerField()
    one_to_three_day = IntegerField()
    three_to_seven_day = IntegerField()
    seven_to_half_month = IntegerField()
    half_to_one_month = IntegerField()


class Car(CreatedBaseModel):
    class FuelType(TextChoices):
        GAS = 'gas', 'Gas'
        ELECTRIC = 'electric', 'Electric'
        HYBRID = 'hybrid', 'Hybrid'

    class TransmissionType(TextChoices):
        MANUAL = 'manual', 'Manual',
        AUTOMATIC = 'automatic', 'Automatic'

    model = CharField(max_length=100)
    brand = ForeignKey('CarBrand', CASCADE, related_name='brand')
    category = ForeignKey('CarCategory', CASCADE, related_name='type')
    color = ForeignKey('CarColor', CASCADE, related_name='color')
    year = DateField()
    deposit = IntegerField(default=0)
    limit_km = IntegerField(default=0)
    fuel_type = CharField(max_length=15, choices=FuelType.choices, default=FuelType.GAS)
    transmission_type = CharField(max_length=15, choices=TransmissionType.choices, default=TransmissionType.AUTOMATIC)
    features = ManyToManyField('apps.Feature', through='apps.CarFeature')
    is_available = BooleanField(default=True)
    author = ForeignKey('apps.User', CASCADE, related_name='author')

    def __str__(self):
        return self.model


class CarFeature(UUIDBaseModel):
    car = ForeignKey("apps.Car", CASCADE)
    feature = ForeignKey("apps.Feature", CASCADE)


class CarImage(UUIDBaseModel):
    car = ForeignKey('Car', CASCADE, related_name='images')
    image = ImageField(upload_to='car/images/%Y/%m/%d/')


class Feature(UUIDBaseModel):
    icon = ImageField(upload_to='car/icons/features/%Y/%m/%d/')
    name = CharField(max_length=155)
    description = CharField(max_length=155)

    def __str__(self):
        return self.name


class Reviews(UUIDBaseModel):
    car = ForeignKey('apps.Car', CASCADE, related_name='reviews')
    user = ForeignKey('apps.User', CASCADE, related_name='reviews')
    stars = IntegerField()
    comment = CKEditor5Field()
