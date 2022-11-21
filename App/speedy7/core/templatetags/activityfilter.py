from django import template
from datetime import datetime, timedelta
from dateutil import tz
from dateutil.parser import parse

register = template.Library()


@register.filter
def activityfilter(date,minutes):
    now = datetime.now(tz=tz.gettz("UTC"))
    since = now - timedelta(minutes=minutes)
    
    return date > since
