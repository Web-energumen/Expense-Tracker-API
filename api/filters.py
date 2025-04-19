from datetime import timedelta

from django.utils import timezone
from django_filters import rest_framework as filters

from .models import Expense


class ExpenseFilter(filters.FilterSet):
    date_range = filters.CharFilter(method='filter_by_date_range')
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')
    category = filters.CharFilter(field_name='category', lookup_expr='icontains')

    class Meta:
        model = Expense
        fields = ['date_range', 'start_date', 'end_date', 'category']

    def filter_by_date_range(self, queryset, name, value):
        today = timezone.now().date()
        print(today)
        if value == 'past_week':
            start_date = today - timedelta(days=7)
        elif value == 'past_month':
            start_date = today - timedelta(days=30)
        elif value == 'last_3_months':
            start_date = today - timedelta(days=90)
        else:
            return queryset

        return queryset.filter(date__gte=start_date, date__lte=today)
