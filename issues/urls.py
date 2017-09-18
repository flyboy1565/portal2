from django.conf.urls import url
from django.contrib import admin

from .views import infowindow

urlpatterns = [
    # url(r'^$', IssueListAPIView.as_view(), name='issue-list'),
    url(r'^(?P<id>[\d-]+)/$', infowindow),
]