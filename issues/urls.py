from django.conf.urls import url
from django.contrib import admin

from .views import infowindow, store_search, edit_issue

urlpatterns = [
    # url(r'^$', IssueListAPIView.as_view(), name='issue-list'),
    url(r'^(?P<id>[\d-]+)/$', infowindow),
    url(r'^edit/$', edit_issue),
    url(r'^edit/(?P<id>[\d-]+)/$', edit_issue, name='edit_issue'),
    url(r'^search/(?P<store>[\d-]+)/$', store_search),
]