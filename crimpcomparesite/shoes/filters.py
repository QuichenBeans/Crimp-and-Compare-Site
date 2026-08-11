import django_filters
from django.db.models import Q, Min, Max
from .models import Shoe, Category
from django import forms


class ShoeSearch(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search_bar', label='Search')

    class Meta:
        model = Shoe
        fields = ['q']

    def search_bar(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(name__icontains=value)|
                Q(brand__icontains=value)|
                Q(category__name__icontains=value)
            ).distinct()
        return queryset.none()


class ShoeFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category__name',
        to_field_name='name',
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Categories'
    )

    in_stock = django_filters.BooleanFilter(
        method='filter_in_stock',
        widget=forms.CheckboxInput,
        label='Only show in stock items',
        required=False
    )
    
    order_by = django_filters.OrderingFilter(
        fields=(
            ('brand', 'brand'),
            ('name', 'name'),
            ('offers__price', 'price'),
        ),
        field_labels={
            'brand': 'Brand (A-Z)',
            '-brand': 'Brand (Z-A)',
            'name': 'Name (A-Z)',
            '-name': 'Name (Z-A)',
            'offers__price': 'Price (Low to High)',
            '-offers__price': 'Price (High to Low)',
        },
        label='Sort by'
    )
    
    
    class Meta:
        model = Shoe
        fields = ['category']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(offers__in_stock=True).distinct()
        return queryset