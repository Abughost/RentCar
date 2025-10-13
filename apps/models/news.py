from django.db.models import CharField, ImageField, TextField

from apps.models.base import CreatedBaseModel


class New(CreatedBaseModel):
    title = CharField(max_length=255)
    description = TextField()  # TODO ckeditor5
    image = ImageField(upload_to='news/%Y/%m/%d/')
