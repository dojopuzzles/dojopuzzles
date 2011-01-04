#-*- coding: utf-8 -*-
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from dojopuzzles.contribuicoes.forms import ContribuicaoForm

def contribuicao(request):
    if request.method == 'POST':
        form = ContribuicaoForm(request.POST)
        if form.is_valid():
            send_mail(form.cleaned_data['assunto'], form.cleaned_data['mensagem'], 
                      form.cleaned_data['email'], ['rennerocha@gmail.com'], 
                      fail_silently=False)
            return HttpResponseRedirect(reverse('contribuicao-recebida'))
    else:
        form = ContribuicaoForm()

    return render_to_response('contribua.html', 
                              locals(), 
                              RequestContext(request))
                              
def contribuicao_recebida(request):
    messages.add_message(request, messages.INFO, 'Mensagem enviada com sucesso. Obrigado pelo contato!')
    return render_to_response('index.html', 
                              locals(), 
                              RequestContext(request))
