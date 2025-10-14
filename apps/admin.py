from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.models import Group

from apps.models import Car, User, CarBrand, CarCategory, Feature, CarFeature, CarImage
from apps.models.cars import CarColor
from apps.models.news import New


class CarImageStackedInline(StackedInline):
    model = CarImage
    extra = 1
    max_num = 8
    min_num = 1

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = 'id', 'phone',

@admin.register(Car)
class CarAdminModel(ModelAdmin):
    list_display = 'model', 'brand','daily_price','category','transmission_type','fuel_type','is_available'

@admin.register(CarBrand)
class CarBrandAdminModel(ModelAdmin):
    list_display = 'name',

@admin.register(CarColor)
class CarColorAdminModel(ModelAdmin):
    list_display = 'name',

@admin.register(CarCategory)
class CarTypeAdminModel(ModelAdmin):
    list_display = 'name',

@admin.register(CarFeature)
class CarFeatureModelAdmin(ModelAdmin):
    list_display = 'id','car','feature'

@admin.register(Feature)
class FeatureModelAdmin(ModelAdmin):
    list_display = 'id','name','icon'


@admin.register(CarImage)
class CarImageModelAdmin(ModelAdmin):
    list_display = 'id', 'car', 'image'

@admin.register(New)
class NewModelAdmin(ModelAdmin):
    list_display = 'id','title'




admin.site.unregister(Group)