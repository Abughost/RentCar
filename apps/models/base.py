import uuid

from django.db.models import Model, Func
from django.db.models.fields import UUIDField, DateTimeField


class GenRandomUUID(Func):
    function = 'gen_random_uuid'
    template = '%(function)s()'
    output_fields = UUIDField()


class CustomUuidModel(Model):
    id = UUIDField(primary_key=True, default=GenRandomUUID(),editable=False)

class CustomDataCreationModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
