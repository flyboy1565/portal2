from django.conf.urls import url
from django.contrib import admin

from .views import (
    IssueDetailAPIView, IssueListAPIView
)
  

urlpatterns = [
    url(r'^$', IssueListAPIView.as_view(), name='issue-list'),
    url(r'^(?P<id>[\w-]+)/$', IssueDetailAPIView.as_view(), name='issue-detail'),
]