from django.db.models import CharField, IntegerField, ImageField, ForeignKey, CASCADE, ManyToManyField, TextChoices, \
    DateField, BooleanField
from django.utils.translation import gettext_lazy as _

from apps.models.base import CreatedBaseModel, UUIDBaseModel, BaseVerboseModel


class CarType(UUIDBaseModel):
    name = CharField(max_length=50)

    def __str__(self):
        return self.name




class CarBrand(UUIDBaseModel, BaseVerboseModel):
    name = CharField(max_length=50)
    logo = ImageField(upload_to='car/icons/brand_logo/%Y/%m/%d/')

    def __str__(self):
        return self.name

class CarColor(UUIDBaseModel, BaseVerboseModel):
    name = CharField(max_length=155)

    def __str__(self):
        return self.name

class CarPrice(CreatedBaseModel):
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
    type = ForeignKey('CarType', CASCADE, related_name='type')
    color = ForeignKey('CarColor',CASCADE,related_name='color')  # TODO fk qilish kk
    year = DateField()
    deposit = IntegerField(default=0)
    limit_km = IntegerField(default=0)
    daily_price = IntegerField()
    fuel_type = CharField(max_length=15, choices=FuelType.choices, default=FuelType.GAS)
    transmission_type = CharField(max_length=15, choices=TransmissionType.choices, default=TransmissionType.AUTOMATIC)
    features = ManyToManyField('apps.Feature', through='apps.CarFeature')
    is_available = BooleanField(default=True)



class CarImage(UUIDBaseModel, BaseVerboseModel):
    car = ForeignKey('Car', CASCADE, related_name='images')
    image = ImageField(upload_to='car/images/%Y/%m/%d/')

class CarFeature(UUIDBaseModel, BaseVerboseModel):
    car = ForeignKey('Car', CASCADE)
    feature = ForeignKey('Feature', CASCADE)

class Feature(UUIDBaseModel,BaseVerboseModel):
    icon = ImageField(upload_to='car/icons/features/%Y/%m/%d/')
    name = CharField(max_length=155)
    description = CharField(max_length=155)

