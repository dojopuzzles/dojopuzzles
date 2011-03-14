# -*- coding: utf-8 -*-
from django.db.models import Count
from django.template import Library, Node

from dojopuzzles.problemas.models import Problema, ProblemaUtilizado

register = Library()

class ProblemasMaisUtilizadosNode(Node):

    def render(self, context):
        context['problemas_utilizados'] = []
        problemas_utilizados = ProblemaUtilizado.objects.values('problema').annotate(Count('problema'))[:5]
        for problema in problemas_utilizados:
            context['problemas_utilizados'].append(Problema.objects.get(pk=problema['problema']))
        return ''

def get_problemas_mais_utilizados(parser, token):
    return ProblemasMaisUtilizadosNode()
get_problemas_mais_utilizados = register.tag(get_problemas_mais_utilizados)
