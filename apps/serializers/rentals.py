from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import ModelSerializer

from apps.models import Rental


class RentModelSerializer(ModelSerializer):

    class Meta:
        model = Rental
        exclude = 'user',
