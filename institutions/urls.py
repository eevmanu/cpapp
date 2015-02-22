# coding=utf-8

from django.conf.urls import patterns, url

from views import PreCollegeView, WeekView

urlpatterns = patterns(
    'institutions.views',

    url(r'^precolleges/?$', PreCollegeView.list,
        name='institutions_precolleges'),
    url(r'^weeks/?$', WeekView.list,
        name='institutions_weeks'),
    url(r'^precolleges/(?P<pk>[0-9]+)/tasktypes/?$', PreCollegeView.tasktypes_from_precollege,
        name='institutions_tasktypes'),
)
