import django_filters

from apps.shop.models import Product


class ProductFilter(django_filters.FilterSet):
    max_price = django_filters.NumberFilter(field_name='price_current', lookup_expr='lte')
    min_price = django_filters.NumberFilter(field_name='price_current', lookup_expr='gte')
    in_stock = django_filters.NumberFilter(lookup_expr='gte')
    created_at = django_filters.DateTimeFilter(lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['max_price', 'min_price', 'in_stock', 'created_at']
