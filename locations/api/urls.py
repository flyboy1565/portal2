from django.conf.urls import url
from django.contrib import admin

from .views import (
    StoreDetailAPIView, StoreListAPIView, 
    DistrictDetailAPIView, DistrictListAPIView,
    RegionDetailAPIView, RegionListAPIView,
    DivisionListAPIView, DivisionDetailAPIView
)
  

urlpatterns = [
    url(r'^stores/$', StoreListAPIView.as_view(), name='store-list'),
    url(r'^stores/(?P<store_number>[\w-]+)/$', StoreDetailAPIView.as_view(), name='store-detail'),
    url(r'^district/$', DistrictListAPIView.as_view(), name='district-list'),
    url(r'^district/(?P<district_number>[\w-]+)/$', DistrictDetailAPIView.as_view(), name='district-detail'),
    url(r'^region/$', RegionListAPIView.as_view(), name='region-list'),
    url(r'^region/(?P<region_number>[\w-]+)/$', RegionDetailAPIView.as_view(), name='region-detail'),
]