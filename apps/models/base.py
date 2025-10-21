from django.db.models import Func, Model
from django.db.models.fields import DateTimeField, UUIDField
from django.utils.translation import gettext_lazy as _



class GenRandomUUID(Func):
    function = 'gen_random_uuid'
    template = '%(function)s()'
    output_fields = UUIDField()


class UUIDBaseModel(Model):
    id = UUIDField(primary_key=True, db_default=GenRandomUUID(), editable=False)

    class Meta:
        abstract = True

class CreatedBaseModel(UUIDBaseModel):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
