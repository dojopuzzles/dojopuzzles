# -*- coding: utf-8 -*-
from django.db.models import Count
from django.template import Library, Node

from problemas.models import Problema, ProblemaUtilizado

register = Library()


class ProblemasMaisUtilizadosNode(Node):

    def render(self, context):
        context['problemas_utilizados'] = []

        problemas_utilizados = ProblemaUtilizado.objects.all().values('problema').annotate(Count('problema')).order_by('-problema__count')[:5]
        problemas = []
        for problema in problemas_utilizados:
            problemas.append(Problema.objects.get(pk=problema['problema']))
        context['problemas_utilizados'] = sorted(problemas, key=lambda a: a.utilizacoes, reverse=True)
        return ''


def get_problemas_mais_utilizados(parser, token):
    return ProblemasMaisUtilizadosNode()
get_problemas_mais_utilizados = register.tag(get_problemas_mais_utilizados)
