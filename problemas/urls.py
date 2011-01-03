#!-*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from dojopuzzles.problemas.models import Problema

urlpatterns = patterns('',
    url(r'^$', 'dojopuzzles.problemas.views.problema_aleatorio', name='problema-aleatorio'),
    url(r'^(?P<problema_id>\d+)/$', 'dojopuzzles.problemas.views.exibe_problema', name='exibe-problema'), 
    url(r'^todos_visualizados/$', 'dojopuzzles.problemas.views.sem_problemas_novos', name='sem-problemas-novos'),
    url(r'^nenhum_problema/$', 'dojopuzzles.problemas.views.sem_problemas', name='nenhum-problema-cadastrado'),
    url(r'^todos/$', 'django.views.generic.list_detail.object_list',
        {'queryset':Problema.objects.all().order_by('titulo'),
         'paginate_by': 15},  name='todos-problemas'),
)
