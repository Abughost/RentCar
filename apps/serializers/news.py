from rest_framework.serializers import ModelSerializer
from yaml.serializer import Serializer

from apps.models.news import New


class NewsModelSerializer(ModelSerializer):
    class Meta:
        model = New
        fields = 'title','description','image'