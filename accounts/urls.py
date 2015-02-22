# coding=utf-8

from django.conf.urls import patterns, url

from .views import AccountView

urlpatterns = patterns(
    'accounts.views',

    url(r'^accounts/signup/?$', AccountView.signup,
        name='signup'),
    url(r'^accounts/signin/?$', AccountView.signin,
        name='signin'),
    url(r'^accounts/signout/?$', AccountView.signout,
        name='signout'),
    url(r'^accounts/(?P<pk>[0-9]+)/?$', AccountView.detail,
        name='update_account_fields'),
    url(r'^accounts/password/reset/?$', AccountView.reset_password,
        name='password_reset_processes'),

    url(r'^accounts/(?P<pk>[0-9]+)/active_ticket/?$', AccountView.get_active_ticket,
        name='active_ticket'),

)
