from django.db.models import CharField, TextField, ImageField

from apps.models.base import UUIDBaseModel, CreatedBaseModel


class New(CreatedBaseModel):
    title = CharField(max_length=255)
    description = TextField()  # TODO ckeditor5
    image = ImageField(upload_to='news/%Y/%m/%d/')
