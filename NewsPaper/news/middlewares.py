import pytz

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')  # trying to pick up the time zone from the session
        #  if it is in the session, then we set this time zone. If it is not there, then it is not installed, and the time zone should be set to default (for server time)
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)

