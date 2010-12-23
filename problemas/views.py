#!-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from dojo.problemas.models import Problema

import simplejson

def problema_aleatorio(request):
    """ Exibe um problema aleatório da lista de problemas cadastrados """
    numero_problemas = len(Problema.objects.all())

    if numero_problemas == 0:
        return HttpResponseRedirect(reverse('nenhum-problema-cadastrado'))

    problemas_visualizados = []
    if "problemas_visualizados" in request.COOKIES:
        problemas_visualizados = request.COOKIES.get('problemas_visualizados', [])
        if problemas_visualizados != []:
            problemas_visualizados = simplejson.loads(problemas_visualizados)

    if len(problemas_visualizados) == numero_problemas:
        return HttpResponseRedirect(reverse('sem-problemas-novos'))

    # Este modo de obter um registro aleatório é considerado muito
    # lento pela documentação do Django. É necessário fazer uma
    # solução melhor.
    problema_escolhido = Problema.objects.order_by('?')[0]
    if problema_escolhido.id in problemas_visualizados:
        while problema_escolhido.id in problemas_visualizados:
            problema_escolhido = Problema.objects.order_by('?')[0]

    return HttpResponseRedirect(reverse('exibe-problema', args=[problema_escolhido.id]))        

def exibe_problema(request, problema_id):
    """ Exibe o problema informado """
    try:
        problema = Problema.objects.get(pk = problema_id)

        if "problemas_visualizados" in request.COOKIES:
            problemas_visualizados = request.COOKIES.get('problemas_visualizados', [])
            if problemas_visualizados != []:
                problemas_visualizados = simplejson.loads(problemas_visualizados)
                if problema.id not in problemas_visualizados:
                    problemas_visualizados.append(problema.id)
        else:
            problemas_visualizados = [problema.id]

        response = render_to_response('problema.html', locals(), RequestContext(request))
        response.set_cookie("problemas_visualizados", problemas_visualizados)

    except Problema.DoesNotExist:
        raise Http404

    return response

def sem_problemas_novos(request):
    """ Exibido se todos os problemas cadastrados já tiverem sido exibidos """
    return render_to_response('sem_problemas_novos.html', locals(), RequestContext(request))
    
def sem_problemas(request):
    """ Exibido se nenhum problema estiver cadastrado no sistema """
    return render_to_response('sem_problemas.html', locals(), RequestContext(request))
