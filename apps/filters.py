from django_filters import FilterSet, NumberFilter, CharFilter

from apps.models import Car


class CarPriceFilter(FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    type = CharFilter(field_name='type__name',lookup_expr='icontains')
    brand_name = CharFilter(field_name='brand__brand_name',lookup_expr='icontains')

    class Meta:
        model = Car
        fields = 'model','type','brand_name','fuel_type'

