from django.conf.urls import url
from .views import report

urlpatterns = [
    url(r'^$', report, name='insanity_report'),
]
