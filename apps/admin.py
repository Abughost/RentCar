from unicodedata import category

from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from apps.models import (Car, CarBrand, CarCategory, CarFeature, CarImage,
                         CarPrice, Feature, User)
from apps.models.cars import CarColor
from apps.models.news import New
from root.settings import MEDIA_URL


class CarImageStackedInline(StackedInline):
    model = CarImage
    extra = 1



@admin.register(Car)
class CarAdminModel(ModelAdmin):
    inlines = [CarImageStackedInline]
    list_display = 'model', 'brand','category','daily_price','deposit','transmission_type','fuel_type','is_available',"car_image"
    list_filter = 'model','brand','category'
    readonly_fields = ['car_image']
    list_select_related = 'brand','category','color'

    def daily_price(self, obj):
        price = CarPrice.objects.filter(car=obj.id).first()
        return price.daily_price if price else "_"



    def car_image(self,obj):
        photos = CarImage.objects.filter(car_id = obj.id)
        if photos.exists():
            imgs = "".join([f'<img src="{photo.image.url}" width="50" height="50" style="margin:2px;" />' for photo in photos])
        else:
            imgs = f'<img src="/media/car/noimage.png" width="50" height="50" style="margin:2px;" />'
        return mark_safe(imgs)


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = 'id', 'phone',


@admin.register(CarBrand)
class CarBrandAdminModel(ModelAdmin):
    list_display = 'name',

@admin.register(CarColor)
class CarColorAdminModel(ModelAdmin):
    list_display = 'name',

@admin.register(CarCategory)
class CarTypeAdminModel(ModelAdmin):
    list_display = 'name',

@admin.register(Feature)
class FeatureModelAdmin(ModelAdmin):
    list_display = 'id','name','icon'


@admin.register(CarImage)
class CarImageModelAdmin(ModelAdmin):
    list_display = 'id', 'car', 'image'

@admin.register(CarPrice)
class CarPriceModelAdmin(ModelAdmin):
    list_display = 'id', 'car__model','daily_price'

@admin.register(CarFeature)
class CarFeatureModelAdmin(ModelAdmin):
    list_display = 'car','feature'

@admin.register(New)
class NewModelAdmin(ModelAdmin):
    list_display = 'id','title'




admin.site.unregister(Group)