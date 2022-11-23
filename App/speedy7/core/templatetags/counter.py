from django import template
from datetime import datetime, timedelta
from dateutil import tz
from dateutil.parser import parse

register = template.Library()


@register.filter
def counter(self):
    return len(self)
