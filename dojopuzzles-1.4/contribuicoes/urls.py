#!-*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^contribua/$', 'contribuicoes.views.contribuicao', name='contribua'),
    url(r'^recebida/$', 'contribuicoes.views.contribuicao_recebida', name='contribuicao-recebida'),
)
