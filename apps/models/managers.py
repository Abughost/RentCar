from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def _create_user_object(self, contact, password, **extra_fields):
        user = self.model(contact=contact, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, contact, password, **extra_fields):

        user = self._create_user_object(contact, password, **extra_fields)
        user.save(using=self._db)
        user.set_unusable_password()
        return user

    def create_superuser(self, contact, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('role',self.model.UserRole.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(contact, password, **extra_fields)


