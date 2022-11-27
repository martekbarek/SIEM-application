from django import template
from datetime import datetime, timedelta
from dateutil import tz
import logging
from dateutil.parser import parse
import pytz


register = template.Library()


@register.filter
def activityfilter(date,minutes):
    now = datetime.now()
    since = now - timedelta(minutes=minutes)
    try:
        return date > since
    except Exception:
        logging.warning("Compared offset-naive and offset-aware datetimes")
        return date.replace(tzinfo=None) > since.replace(tzinfo=None)
        