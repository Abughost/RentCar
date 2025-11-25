from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer
from yaml.serializer import Serializer

from apps.models.news import New


class NewsModelSerializer(ModelSerializer):
    author = CurrentUserDefault()

    class Meta:
        model = New
        fields = 'id', 'title', 'description', 'image',