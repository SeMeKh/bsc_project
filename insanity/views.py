from django.conf import settings
from django.shortcuts import render

from insanity.apps import all_stats


def report(request):
    return render(request, 'report.html', {'all_stats': all_stats, 'SENTRY_URL': settings.SENTRY_URL})
