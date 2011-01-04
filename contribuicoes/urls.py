#!-*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^contribua/$', 'dojopuzzles.contribuicoes.views.contribuicao', name='contribua'),
    url(r'^recebida/$', 'dojopuzzles.contribuicoes.views.contribuicao_recebida', name='contribuicao-recebida'),
)
