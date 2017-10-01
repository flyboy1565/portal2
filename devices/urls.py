from django.conf.urls import url
from django.contrib import admin

from .views import get_all, get_one

urlpatterns = [
    url(r'^$', get_all, name='devices'),
    url(r'^(?P<id>[\d-]+)/$', get_one, name='device'),
]