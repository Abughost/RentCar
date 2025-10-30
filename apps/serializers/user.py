from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer

from apps.models import User, UserProfile


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'phone'

class VerifiedUserModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = UserProfile
        exclude = ()
