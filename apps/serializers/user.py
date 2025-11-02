from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import ModelSerializer

from apps.models import User, UserProfile


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'contact','first_name','last_name'

class VerifiedUserModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = UserProfile
        exclude = ()
