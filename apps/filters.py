from django_filters import CharFilter, FilterSet, NumberFilter

from apps.models import Car


class CarPriceFilter(FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    type = CharFilter(field_name='type__name',lookup_expr='icontains')
    brand_uuid = CharFilter(field_name='brand__brand_name',lookup_expr='icontains')

    class Meta:
        model = Car
        fields = 'model','type','brand_uuid','fuel_type','is_available'

