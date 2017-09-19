from django.conf.urls import url
from django.contrib import admin

from .views import (
    KitListAPIView
)
  
urlpatterns = [
    url(r'^$', KitListAPIView.as_view(), name='kit-list'),
]  