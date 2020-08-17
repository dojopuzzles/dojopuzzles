# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from problemas.models import ProblemaUtilizado

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^problemas/', include('problemas.urls')),
    (r'^contribuicoes/', include('contribuicoes.urls')),

    url(r'^$', 'django.views.generic.simple.direct_to_template',
        {'template': 'index.html',
         'extra_context': {'problemas_utilizados': ProblemaUtilizado.objects.count}},
         name='inicio'),
    url(r'^sobre/$', 'django.views.generic.simple.direct_to_template',
        {'template': 'sobre.html', 'extra_context': {'titulo_pagina': 'Sobre'}}, name='sobre'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
