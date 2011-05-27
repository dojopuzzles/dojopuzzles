#!-*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from dojopuzzles.problemas.models import Problema

urlpatterns = patterns('',
    url(r'^$', 'dojopuzzles.problemas.views.problema_aleatorio', name='problema-aleatorio'),
    url(r'^exibe/(?P<slug>[\w_-]+)/$', 'dojopuzzles.problemas.views.exibe_problema', name='exibe-problema'),
    url(r'^busca/$', 'dojopuzzles.problemas.views.busca_problema_por_titulo', name='busca-problema-por-titulo'),
    url(r'^(?P<problema_id>\d+)/$', 'dojopuzzles.problemas.views.exibe_problema_pelo_id', name='exibe-problema-pelo-id'),
    url(r'^gostei/(?P<problema_id>\d+)/$', 'dojopuzzles.problemas.views.problema_utilizado', name='problema-utilizado-em-dojo'),
    url(r'^todos_visualizados/$', 'dojopuzzles.problemas.views.sem_problemas_novos', name='sem-problemas-novos'),
    url(r'^nenhum_problema/$', 'dojopuzzles.problemas.views.sem_problemas', name='nenhum-problema-cadastrado'),
    url(r'^todos/$', 'django.views.generic.list_detail.object_list',
        {'queryset':Problema.objects.filter(publicado=True).order_by('titulo'),
         'paginate_by': 15, 'extra_context':{'titulo_pagina': 'Problemas cadastrados'}},  name='todos-problemas'), 
)
