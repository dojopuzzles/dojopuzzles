#!-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list

from problemas.models import Problema
from problemas.forms import FormBusca


def problema_aleatorio(request):
    """ Exibe um problema aleatório da lista de problemas cadastrados """
    numero_problemas = len(Problema.objects.all())

    if numero_problemas == 0:
        return HttpResponseRedirect(reverse('nenhum-problema-cadastrado'))

    problemas_visualizados = []
    if 'problemas_visualizados' in request.session:
        problemas_visualizados = request.session['problemas_visualizados']

    problemas_nao_gostei = []
    if 'problemas_que_nao_gostei' in request.session:
        problemas_nao_gostei = request.session['problemas_que_nao_gostei']

    if 'nao_gostei' in request.GET:
        problema_nao_gostei = Problema.objects.get(pk=int(request.GET['nao_gostei']))
        if problema_nao_gostei in problemas_visualizados:
            problemas_visualizados.remove(problema_nao_gostei)
            request.session['problemas_visualizados'] = problemas_visualizados
        if problema_nao_gostei not in problemas_nao_gostei:
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
    problemas = Problema.objects.exclude(id__in=ids_problemas_visualizados).exclude(id__in=ids_problemas_nao_gostei).exclude(publicado=False).order_by('?')
    if(len(problemas) == 0):
        return HttpResponseRedirect(reverse('sem-problemas-novos'))
    else:
        problema_escolhido = problemas[0]
    return HttpResponseRedirect(reverse('exibe-problema', args=[problema_escolhido.slug]))


def exibe_problema(request, slug):
    """ Exibe o problema informado """
    problema = get_object_or_404(Problema, slug=slug, publicado=True)

    problemas_visualizados = []
    if 'problemas_visualizados' in request.session:
        problemas_visualizados = request.session['problemas_visualizados']
    problemas_visualizados.append(problema)
    problemas_visualizados = list(set(problemas_visualizados))
    request.session['problemas_visualizados'] = problemas_visualizados
    titulo_pagina = problema.titulo

    return render_to_response('problema.html', locals(), RequestContext(request))


def exibe_problema_pelo_id(request, problema_id):
    problema = get_object_or_404(Problema, pk=problema_id)
    return HttpResponseRedirect(reverse('exibe-problema', args=[problema.slug]))


def sem_problemas_novos(request):
    """ Exibido se todos os problemas cadastrados já tiverem sido exibidos """
    problemas_visualizados = []
    if 'problemas_visualizados' in request.session:
        problemas_visualizados = request.session['problemas_visualizados']
    titulo_pagina = 'Todos os problemas visualizados'
    return render_to_response('sem_problemas_novos.html', locals(), RequestContext(request))


def sem_problemas(request):
    """ Exibido se nenhum problema estiver cadastrado no sistema """
    titulo_pagina = 'Nenhum problema cadastrado'
    return render_to_response('sem_problemas.html', locals(), RequestContext(request))


def problema_utilizado(request, problema_id):
    problema = get_object_or_404(Problema, pk=problema_id)
    problema.utilizar()
    request.session['problema_utilizado'] = problema
    return HttpResponseRedirect(reverse('exibe-problema', args=[problema.slug]))


def busca_problema_por_titulo(request):
    if request.method == 'POST':
        form = FormBusca(request.POST)
        if form.is_valid():
            titulo = form.data['titulo'].strip()
            if len(titulo) > 0:
                problema = Problema.objects.filter(titulo__icontains=titulo, publicado=True)
                if len(problema) == 1:
                    return HttpResponseRedirect(reverse('exibe-problema', args=[problema[0].slug]))
                retorno_args = {'queryset': problema, 'paginate_by': 15, 'extra_context': {'titulo_pagina': 'Busca de Problemas', 'acao': 'busca', 'titulo_busca': titulo}}
                return object_list(request, **retorno_args)

    return HttpResponseRedirect(reverse('todos-problemas'))
