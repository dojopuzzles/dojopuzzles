#!-*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('dojo.problemas.views',
    url(r'^$', 'problema_aleatorio', name='problema-aleatorio'),
    url(r'^(?P<problema_id>\d+)/$', 'exibe_problema', name='exibe-problema'), 
    url(r'^todos_visualizados/$', 'sem_problemas_novos', name='sem-problemas-novos'),
    url(r'^nenhum_problema/$', 'sem_problemas', name='nenhum-problema-cadastrado'),
)
