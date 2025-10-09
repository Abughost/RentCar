from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group

from apps.models import Car, User


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = 'id','phone',

@admin.register(Car)
class CarAdmin(ModelAdmin):
    list_display = 'brand',

admin.site.unregister(Group)