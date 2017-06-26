from django.conf.urls import url
from django.contrib import admin

from .views import PhoneBillingDetailAPIView, PhoneBillingListAPIView

urlpatterns = [
    url(r'^$', PhoneBillingListAPIView.as_view(), name='store-phone-list'),
    url(r'^(?P<store_number>[\w-]+)/$', PhoneBillingDetailAPIView.as_view(), name='store-phone-detail'),
]
