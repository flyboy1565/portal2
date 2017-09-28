from django.conf.urls import url
from django.contrib import admin

from .views import (get_all, get_one, create_new, request_return,
                new_shipment, return_shipment, add_tracking, lost_shipment,
                )

urlpatterns = [
    url(r'^$', get_all, name='kits'),
    url(r'^(?P<id>[\d-]+)/$', get_one, name='kit'),
    url(r'^create/$', create_new, name='create_kit'),
    url(r'^shipment/(?P<id>[\d-]+)/$', new_shipment, name='new_shipment'),
    url(r'^request/(?P<kit_id>[\d-]+)/$', request_return, name='request_return'),
    url(r'^return/(?P<id>[\d-]+)/$', return_shipment, name='return_shipment'),
    url(r'^lost/(?P<id>[\d-]+)/$', lost_shipment, name='lost_shipment'),
    url(r'^add_tracking/(?P<kit_id>[\d-]+)/(?P<ship_type>[\w+]+)/$', add_tracking, name='add_track'),
]


