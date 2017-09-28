from django.conf.urls import url
from django.contrib import admin

from .views import (
    infowindow, store_search, edit_issue, additional_issues,
    report_total_down, new_additional_issue, close_additional
    )

urlpatterns = [
    # url(r'^$', IssueListAPIView.as_view(), name='issue-list'),
    url(r'^(?P<id>[\d-]+)/$', infowindow),
    url(r'^edit/$', edit_issue),
    url(r'^edit/(?P<id>[\d-]+)/$', edit_issue, name='edit_issue'),
    url(r'^search/(?P<store>[\d-]+)/$', store_search, name='store_search'),
    url(r'^additional/$', additional_issues, name='additional_issues'),
    url(r'^new_additional/$', new_additional_issue, name='new_additional_issue'),
    url(r'^close_additional/(?P<id>[\d-]+)/$', close_additional, name='close_additional'),
    url(r'^report/previous_day/$', report_total_down, name='previous_day'),
    
]