from django.db.models import CharField, ImageField, TextField

from apps.models.base import CreatedBaseModel, UUIDBaseModel


class News(UUIDBaseModel, CreatedBaseModel):
    title = CharField(max_length=255)
    description = TextField()
    image = ImageField(upload_to='news/%Y/%m/%d/')
