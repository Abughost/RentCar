from django.db.models import Func, Model
from django.db.models.fields import DateTimeField, UUIDField
from django.utils.translation import gettext_lazy as _
from jsonschema.exceptions import ValidationError
from rest_framework.permissions import BasePermission


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

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.is_superuser

class IsRegisteredUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active and request.user.is_registered
