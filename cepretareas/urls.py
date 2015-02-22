from django.conf.urls import patterns, include, url
from django.contrib import admin

# no needed since 1.7
# admin.autodiscover()

urlpatterns = patterns(
    '',

    # url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^s3direct/', include('s3direct.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^', include('institutions.urls')),
    url(r'^', include('tasks.urls')),
    url(r'^', include('enrollments.urls')),

)
