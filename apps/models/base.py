from django.db.models import Func, Model
from django.db.models.fields import DateTimeField, UUIDField
from django.utils.translation import gettext_lazy as _



class GenRandomUUID(Func):
    function = 'gen_random_uuid'
    template = '%(function)s()'
    output_fields = UUIDField()


class UUIDBaseModel(Model):
    id = UUIDField(primary_key=True, default=GenRandomUUID(), editable=False)

    class Meta:
        abstract = True

class BaseVerboseModel(Model):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        verbose = cls.__name__.replace('_',' ')
        verbose = ''.join([' '+char if char.isupper() else char for char in verbose]).strip().title()

        if not hasattr(cls._meta, 'verbose_name'):
            cls._meta.verbose_name = _(verbose)
        if not hasattr(cls._meta, 'verbose_name_plural'):
            cls._meta.verbose_name_plural = _(f'{verbose}s')

    class Meta:
        abstract = True


class CreatedBaseModel(UUIDBaseModel, BaseVerboseModel):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
