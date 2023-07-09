import django_filters
from .models import Product, Order
from django import forms


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['code', 'name', 'date_created']

    code = django_filters.CharFilter(lookup_expr='icontains', label='Код', widget=forms.TextInput(
        attrs={'class': 'filter-forms form-control form-control-sm'}))
    name = django_filters.ModelChoiceFilter(queryset=Product.objects.all(), empty_label='Назва Продукту', widget=forms.Select(
         attrs={'class': 'filter-forms form-select form-select-sm'}))
