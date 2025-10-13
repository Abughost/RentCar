from django.db.models import ForeignKey, CASCADE, IntegerField, BooleanField
from rest_framework.fields import DateTimeField

from apps.models.base import CreatedBaseModel


class Rental(CreatedBaseModel):
    car = ForeignKey('apps.Car',CASCADE, related_name='car')
    user = ForeignKey('apps.User', CASCADE, related_name='user')
    start_data = DateTimeField()
    end_data = DateTimeField()
    total_price = IntegerField()
    is_paid = BooleanField(default=False)
