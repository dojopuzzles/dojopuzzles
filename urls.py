#!-*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'problemas/', include('dojopuzzles.problemas.urls')),
    url(r'^$', 'django.views.generic.simple.direct_to_template',
        {'template': 'index.html'}, name='inicio'),
    url(r'^contribua/$', 'django.views.generic.simple.direct_to_template',
        {'template': 'index.html'}, name='contribua'),
    url(r'^sobre/$', 'django.views.generic.simple.direct_to_template',
        {'template': 'sobre.html'}, name='sobre'),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    url(r'^media/(.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
