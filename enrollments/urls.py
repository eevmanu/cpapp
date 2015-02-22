# coding=utf-8

from django.conf.urls import patterns, url

from .views import TicketView

urlpatterns = patterns(
    'enrollments.views',

    url(r'^tickets/?$', TicketView.list,
        name='create_ticket'),
    url(r'^tickets/(?P<pk>[0-9]+)/cancel?$', TicketView.cancel_ticket,
        name='cancel_ticket'),

)
