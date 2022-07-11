from django import template
from datetime import datetime

import locale


locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)


register = template.Library()


@register.simple_tag()
def current_time(format_string='%A %d %B %Y'):
   return datetime.utcnow().strftime(format_string)

