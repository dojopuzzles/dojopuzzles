#!-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from problemas.models import Problema

def problema_aleatorio(request):
    """ Exibe um problema aleatório da lista de problemas cadastrados """

    # Este modo de obter um registro aleatório é considerado muito
    # lento pela documentação do Django. É necessário fazer uma
    # solução melhor.
    problema_escolhido = Problema.objects.order_by('?')[0]

    return HttpResponseRedirect(reverse('exibe-problema', args=[problema_escolhido.id]))

def exibe_problema(request, problema_id):
    """
        Exibe o problema informado e armazena um COOKIE no browser
        indicando os problemas que já foram visualizados.
    """
    try:
        problema = Problema.objects.get(pk = problema_id)

        if "problemas_visualizados" in request.COOKIES:
            problemas = request.COOKIES["problemas_visualizados"].split(',')
            problemas_visualizados = []
            for id in problemas:
                problemas_visualizados.append(Problema.objects.get(pk=id))
            if str(problema.id) not in problemas:
                print "ei"
                problemas.append(str(problema.id))
            problemas = ','.join(problemas)
        else:
            problemas = str(problema.id)

        response = render_to_response('problema.html', locals(), RequestContext(request))

        response.set_cookie("problemas_visualizados", problemas)
        #response.delete_cookie("problemas_visualizados")

    except Problema.DoesNotExist:
        raise Http404

    return response
