import re

from django.contrib.auth.models import AbstractUser
from django.core.cache import CacheHandler
from django.db.models import (CASCADE, DateField, IntegerField, OneToOneField,
                              TextChoices)
from django.db.models.fields import CharField
from rest_framework.exceptions import ValidationError

from apps.models.base import UUIDBaseModel
from apps.models.managers import CustomUserManager

"""
superuser

admin
user
"""


class User(AbstractUser, UUIDBaseModel):
    phone = CharField(max_length=20, unique=True)
    USERNAME_FIELD = 'phone'

    username = None
    email = None
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def check_phone(self):
        digits = re.findall(r'\d', self.phone)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        self.phone = phone.removeprefix('998')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.check_phone()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class UserProfile(UUIDBaseModel):
    user = OneToOneField('apps.User', CASCADE, related_name='profile')
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    data_of_birth = DateField()
    driver_licence_date_of_issue = DateField()
    id_card_number = CharField(max_length=9)
    personal_number = CharField(max_length=14)
    driver_licence_number = CharField(max_length=9)
