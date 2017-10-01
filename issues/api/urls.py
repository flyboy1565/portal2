from django.conf.urls import url
from django.contrib import admin

from .views import (
    IssueDetailAPIView, IssueListAPIView, UpdateIssueWithWorkOn, WorkOnCompleted
)
  

urlpatterns = [
    url(r'^list/$', IssueListAPIView.as_view(), name='issue-list'),
    url(r'^detail/(?P<id>[\w-]+)/$', IssueDetailAPIView.as_view(), name='issue-detail'),
    url(r'^workon/(?P<id>[\w-]+)/$', UpdateIssueWithWorkOn, name='workon'),
    url(r'^complete/(?P<id>[\w-]+)/$', WorkOnCompleted, name='workon-complete'),
]