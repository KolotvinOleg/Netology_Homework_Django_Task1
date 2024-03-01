from django_filters import rest_framework as filters
from .models import Stock
from django_filters import Filter
from django.db.models import Q


class TitleOrDescription(Filter):
    def filter(self, qs, value):
        if value is not None:
            qs = qs.filter(Q(products__title__icontains=value) | Q(products__description__icontains=value))
        return qs


class StockFilter(filters.FilterSet):
    products = filters.NumberFilter(field_name='products__id', lookup_expr='exact')
    search = TitleOrDescription(field_name='title_or_description')

    class Meta:
        model = Stock
        fields = ['products']
