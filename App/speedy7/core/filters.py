import django_filters

from .models import Log

class LogFilter(django_filters.FilterSet):
    class Meta:
        model = Log
        fields = {'facility': ['exact'], 'host': ['exact']}