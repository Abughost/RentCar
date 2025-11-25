from django.db.models import CASCADE, CharField, DateTimeField, ForeignKey
from django.db.models.enums import TextChoices

from apps.models.base import CreatedBaseModel


class Rental(CreatedBaseModel):
    class PaymentMethod(TextChoices):
        CASH = 'cash', 'Cash'
        CARD = 'card', 'Card'

    car = ForeignKey('apps.Car', CASCADE, related_name='car')
    user = ForeignKey('apps.UserProfile', CASCADE, related_name='rental')
    pick_up_location = CharField(max_length=255)
    pick_up_data_time = DateTimeField()
    drop_of_location = CharField(max_length=255)
    drop_of_data_time = DateTimeField()
    payment_method = CharField(max_length=4, choices=PaymentMethod.choices, default=PaymentMethod.CARD)


