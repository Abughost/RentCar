from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group

from apps.models import Car, User, CarBrand, CarType
from apps.models.cars import CarColor


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = 'id', 'phone',

@admin.register(Car)
class CarAdminModel(ModelAdmin):
    list_display = 'model', 'brand',

@admin.register(CarBrand)
class CarBrandAdminModel(ModelAdmin):
    list_display = 'name',

@admin.register(CarColor)
class CarColorAdminModel(ModelAdmin):
    list_display = 'name',

@admin.register(CarType)
class CarTypeAdminModel(ModelAdmin):
    list_display = 'name',



admin.site.unregister(Group)