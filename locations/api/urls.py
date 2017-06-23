from django.conf.urls import url
from django.contrib import admin

from .views import StoreDetailAPIView, StoreListAPIView, DistrictDetailAPIView, DistrictListAPIView
  

urlpatterns = [
    url(r'^stores/$', StoreListAPIView.as_view(), name='store-list'),
    url(r'^stores/(?P<store_number>[\w-]+)/$', StoreDetailAPIView.as_view(), name='store-detail'),
    url(r'^district/$', DistrictListAPIView.as_view(), name='district-list'),
    url(r'^district/(?P<district_number>[\w-]+)/$', DistrictDetailAPIView.as_view(), name='district-detail'),
]