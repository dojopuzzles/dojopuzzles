#-*- coding: utf-8 -*-
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from dojopuzzles.contribuicoes.forms import ContribuicaoForm

MENSAGEM_AGRADECIMENTO = """
  {0},

  Obrigado por colaborar com o DojoPuzzles.com. O seu problema enviado será analisado e caso realmente atenda aos nossos critérios ele será em breve disponibilizado para todos os nossos visitantes (você será avisado).
        
  Nós tomamos o direito de, a nosso critério, editar o texto dos problemas para:
  - Corrigir de eventuais erros de digitação;
  - Tornar as descrições mais curtas, sem alterar o objetivo do problema

  Caso não concorde com isso, responda esse e-mail informando que não deseja que o corpo do problema seja alterado ou que o problema seja publicado.

  Atenciosamente,
                    
  DojoPuzzles.com"""

def contribuicao(request):
    if request.method == 'POST':
        form = ContribuicaoForm(request.POST)
        if form.is_valid():
            emails_a_enviar = []

            mensagem = form.cleaned_data['mensagem']
            email_administracao = 'contato@dojopuzzles.com'
            remetente = form.cleaned_data['email']

            assunto = form.cleaned_data['assunto']
            if assunto == 'CONTATO':
                subject = 'DojoPuzzles.com - Contato realizado através do site'
                emails_a_enviar.append({'subject': subject,
                                        'message': mensagem,
                                        'from_email': remetente,
                                        'recipient_list': [email_administracao],
                                        'fail_silently': False})

            elif assunto == 'PROBLEMA_NOVO':
                subject = 'DojoPuzzles.com - Obrigado pela contribuição'
                mensagem_agradecimento = MENSAGEM_AGRADECIMENTO.format(form.cleaned_data['nome'])

                emails_a_enviar.append({'subject': subject,
                                        'message': mensagem_agradecimento,
                                        'from_email': email_administracao,
                                        'recipient_list': [remetente],
                                        'fail_silently': False})

                subject = 'DojoPuzzles.com - Nova contribuição de problema'
                emails_a_enviar.append({'subject':subject,
                                        'message': mensagem,
                                        'from_email': remetente,
                                        'recipient_list': [email_administracao],
                                        'fail_silently': False})

            for email in emails_a_enviar:
                send_mail(**email)

            return HttpResponseRedirect(reverse('contribuicao-recebida'))
    else:
        form = ContribuicaoForm()

    titulo_pagina = 'Contribua'
    return render_to_response('contribua.html', 
                              locals(), 
                              RequestContext(request))
                              
def contribuicao_recebida(request):
    messages.add_message(request, messages.INFO, 'Mensagem enviada com sucesso. Obrigado pelo contato!')
    return render_to_response('index.html', 
                              locals(), 
                              RequestContext(request))
