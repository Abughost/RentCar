from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, BooleanField, DateField, OneToOneField,
                              TextChoices)
from django.db.models.fields import CharField

from apps.models.base import UUIDBaseModel
from apps.models.managers import CustomUserManager


class User(AbstractUser, UUIDBaseModel):
    class UserRole(TextChoices):
        ADMIN = 'admin', 'Admin',
        USER = 'user', 'User',
        MODERATOR = 'moderator', 'Moderator'

    role = CharField(max_length=15, choices=UserRole.choices, default=UserRole.USER)
    contact = CharField(max_length=255, unique=True)
    is_registered = BooleanField(default=False, editable=False)

    USERNAME_FIELD = 'contact'
    REQUIRED_FIELDS = []

    username = None
    email = None
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Verified user'
        verbose_name_plural = 'Verified users'

    # def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
    #     if self.is_superuser:
    #         self.role = self.UserRole.ADMIN
    #
    #     if self.pk:
    #         old = User.objects.filter(pk = self.pk).first()
    #         if old and self.password != old.password :
    #             self.password = make_password(self.password)
    #
    #     super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class UserProfile(UUIDBaseModel):
    user = OneToOneField('apps.User', CASCADE, related_name='profile')
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    data_of_birth = DateField()
    driver_licence_date_of_issue = DateField()
    id_card_number = CharField(max_length=9)
    personal_number = CharField(max_length=14)
    driver_licence_number = CharField(max_length=9)

    class Meta:
        verbose_name = 'Registered user'
        verbose_name_plural = 'Registered users'

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.user.is_registered = True
        self.user.save(update_fields=['is_registered'])
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return self.first_name + " " + self.last_name
