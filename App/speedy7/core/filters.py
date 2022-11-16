import django_filters

from .models import *

class LogFilter(django_filters.FilterSet):
    class Meta:
        model = Log
        fields = {'facility', 'host', 'program'}