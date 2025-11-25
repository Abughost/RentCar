from django.db.models import CharField, ImageField, ForeignKey, CASCADE
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import CreatedBaseModel


class New(CreatedBaseModel):
    title = CharField(max_length=255)
    description = CKEditor5Field()
    image = ImageField(upload_to='news/%Y/%m/%d/')
    author = ForeignKey('apps.User', CASCADE, related_name='news')
