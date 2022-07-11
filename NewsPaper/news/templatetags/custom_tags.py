from django import template
from datetime import datetime

import locale


locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)


register = template.Library()


@register.simple_tag()
def current_time(format_string='%A %d %B %Y'):
   return datetime.utcnow().strftime(format_string)

