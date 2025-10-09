from django.db.models import CharField, TextField, ImageField

from apps.models.base import UUIDBaseModel, CreatedBaseModel


class News(UUIDBaseModel, CreatedBaseModel):
    title = CharField(max_length=255)
    description = TextField()
    image = ImageField(upload_to='news/%Y/%m/%d/')
