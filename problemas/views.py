#!-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from dojopuzzles.problemas.models import Problema, ProblemaUtilizado

def problema_aleatorio(request):
    """ Exibe um problema aleatório da lista de problemas cadastrados """
    numero_problemas = len(Problema.objects.all())

    if numero_problemas == 0:
        return HttpResponseRedirect(reverse('nenhum-problema-cadastrado'))

    problemas_visualizados = []
    if request.session.has_key('problemas_visualizados'):
        problemas_visualizados = request.session['problemas_visualizados']

    problemas_nao_gostei = []
    if request.session.has_key('problemas_que_nao_gostei'):
        problemas_nao_gostei = request.session['problemas_que_nao_gostei']
    if 'nao_gostei' in request.GET:
        problema_nao_gostei = Problema.objects.get(pk=int(request.GET['nao_gostei']))
        problemas_visualizados.remove(problema_nao_gostei)
        request.session['problemas_visualizados'] = problemas_visualizados
        problemas_nao_gostei.append(problema_nao_gostei)
        request.session['problemas_que_nao_gostei'] = problemas_nao_gostei

    # TODO Acho que dá para melhorar esse trecho
    ids_problemas_visualizados = []
    for problema in problemas_visualizados:
        ids_problemas_visualizados.append(problema.id)

    ids_problemas_nao_gostei = []
    for problema in problemas_nao_gostei:
        ids_problemas_nao_gostei.append(problema.id)

    # TODO Este modo de obter um registro aleatório é considerado muito
    # lento pela documentação do Django. É necessário fazer uma
    # solução melhor.
    problemas = Problema.objects.exclude(id__in=ids_problemas_visualizados).exclude(id__in=ids_problemas_nao_gostei).order_by('?')
    if(len(problemas) == 0):
        return HttpResponseRedirect(reverse('sem-problemas-novos'))
    else:
        problema_escolhido = problemas[0]
    

    return HttpResponseRedirect(reverse('exibe-problema', args=[problema_escolhido.id]))

def exibe_problema(request, problema_id):
    """ Exibe o problema informado """
    try:
        problema = Problema.objects.get(pk = problema_id)
        
        if 'gostei' in request.GET:
            ProblemaUtilizado(problema=problema).save()
            request.session['problema_utilizado'] = problema

        problemas_visualizados = []
        if request.session.has_key('problemas_visualizados'):
            problemas_visualizados = request.session['problemas_visualizados']
        problemas_visualizados.append(problema)
        problemas_visualizados = list(set(problemas_visualizados))
        request.session['problemas_visualizados'] = problemas_visualizados
        response = render_to_response('problema.html', locals(), RequestContext(request))
    except Problema.DoesNotExist:
        raise Http404
    return response

def sem_problemas_novos(request):
    """ Exibido se todos os problemas cadastrados já tiverem sido exibidos """
    problemas_visualizados = []
    if request.session.has_key('problemas_visualizados'):
        problemas_visualizados = request.session['problemas_visualizados']
    return render_to_response('sem_problemas_novos.html', locals(), RequestContext(request))

def sem_problemas(request):
    """ Exibido se nenhum problema estiver cadastrado no sistema """
    return render_to_response('sem_problemas.html', locals(), RequestContext(request))
