from django.conf.urls import url
from django.contrib import admin

from .views import (
    SystemListAPIView
)
  
urlpatterns = [
    url(r'^$', SystemListAPIView.as_view(), name='system-list'),
]  