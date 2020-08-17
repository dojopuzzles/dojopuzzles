#-*- coding: utf-8 -*-
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from contribuicoes.forms import ContribuicaoForm
from problemas.models import Problema

MENSAGEM_AGRADECIMENTO = """
  {0},

  Obrigado por colaborar com o DojoPuzzles.com. O seu problema enviado será analisado e caso realmente atenda aos nossos critérios ele será em breve disponibilizado para todos os nossos visitantes (você será avisado).

  Nós tomamos o direito de, a nosso critério, editar o texto dos problemas para:
  - Corrigir de eventuais erros de digitação;
  - Tornar as descrições mais curtas, sem alterar o objetivo do problema.

  Caso não concorde com isso, responda esse e-mail informando que não deseja que o corpo do problema seja alterado ou que o problema seja publicado.

  Atenciosamente,

  DojoPuzzles.com"""


def _enviar_email_contato(form, agradecer=False):
    operacao = form.cleaned_data['assunto']
    email = {}

    if agradecer == True:
        email['subject'] = 'DojoPuzzles.com - Obrigado pela contribuição'
        email['message'] = MENSAGEM_AGRADECIMENTO.format(form.cleaned_data['nome'])
        email['recipient_list'] = [form.cleaned_data['email']]
        email['from_email'] = 'contato@dojopuzzles.com'
        send_mail(**email)

    if operacao == 'CONTATO':
        email['subject'] = 'DojoPuzzles.com - Contato realizado através do site'
    elif operacao == 'PROBLEMA_NOVO':
        email['subject'] = 'DojoPuzzles.com - Nova contribuição de problema'

    email['message'] = form.cleaned_data['mensagem']
    email['from_email'] = form.cleaned_data['email']
    email['recipient_list'] = ['contato@dojopuzzles.com']
    email['fail_silently'] = False
    send_mail(**email)


def contribuicao(request):
    form = ContribuicaoForm(request.POST or None)
    if form.is_valid():
        operacao = form.cleaned_data['assunto']

        if operacao == 'CONTATO':
            _enviar_email_contato(form)
        if operacao == 'PROBLEMA_NOVO':
            _enviar_email_contato(form, agradecer=True)
            titulo_problema = form.cleaned_data['titulo_problema']
            descricao_problema = form.cleaned_data['mensagem']
            nome_remetente = form.cleaned_data['nome']
            mensagem = form.cleaned_data['mensagem']
            Problema.objects.create(titulo=titulo_problema,
                                    descricao=mensagem,
                                    nome_contribuidor=nome_remetente,
                                    publicado=False)

        return HttpResponseRedirect(reverse('contribuicao-recebida'))

    titulo_pagina = 'Contribua'
    return render_to_response('contribua.html',
                              locals(),
                              RequestContext(request))


def contribuicao_recebida(request):
    messages.add_message(request, messages.INFO, 'Mensagem enviada com sucesso. Obrigado pelo contato!')
    return render_to_response('index.html',
                              locals(),
                              RequestContext(request))
