#:-*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client

from django.core import mail
from django.core.urlresolvers import reverse

from dojopuzzles.contribuicoes.forms import ContribuicaoForm

class EnvioContribuicaoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
            
    def test_deve_existir_url(self):
        response = self.client.get(reverse('contribua'))
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, "<title>DojoPuzzles.com - Contribua</title>", 1)

    def test_deve_renderizar_formulario_correto(self):
        response = self.client.get(reverse('contribua'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contribua.html')
        self.assertEqual(type(response.context['form']), ContribuicaoForm)

    def test_deve_enviar_email_com_dados_do_formulario_preenchido(self):
        self.assertEqual(len(mail.outbox), 0)
        dados_formulario = {'nome':'Usuario Teste',
                            'email':'usuario@teste.com',
                            'assunto':'CONTATO',
                            'mensagem':'Esta mensagem de teste',}
        response = self.client.post(reverse('contribua'), dados_formulario)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].body, 'Esta mensagem de teste')
        self.assertEqual(mail.outbox[0].subject, 'DojoPuzzles.com - Contato realizado através do site')
        self.assertEqual(mail.outbox[0].from_email, 'usuario@teste.com')
        self.assertEqual(mail.outbox[0].to, ['rennerocha@gmail.com'])
        self.assertRedirects(response, reverse('contribuicao-recebida'))

    def test_deve_enviar_email_de_agradecimento_ao_remetente(self):
        """ Após enviar uma contribuição, o usuário deve receber um e-mail confirmando o recebimento e agradecendo o auxílio """
        self.assertEqual(len(mail.outbox), 0)
        dados_formulario = {'nome':'Usuario Teste',
                            'email':'usuario@teste.com',
                            'assunto':'PROBLEMA_NOVO',
                            'mensagem':'Esta mensagem de teste',}
        response = self.client.post(reverse('contribua'), dados_formulario)
        self.assertEqual(len(mail.outbox), 2)

        from dojopuzzles.contribuicoes.views import MENSAGEM_AGRADECIMENTO
        self.assertEqual(mail.outbox[0].body, MENSAGEM_AGRADECIMENTO.format('Usuario Teste'))
        self.assertEqual(mail.outbox[0].subject, 'DojoPuzzles.com - Obrigado pela contribuição')
        self.assertEqual(mail.outbox[0].from_email, 'contato@dojopuzzles.com')
        self.assertEqual(mail.outbox[0].to, ['usuario@teste.com'])

        self.assertEqual(mail.outbox[1].body, 'Esta mensagem de teste')
        self.assertEqual(mail.outbox[1].subject, 'DojoPuzzles.com - Nova contribuição de problema')
        self.assertEqual(mail.outbox[1].from_email, 'usuario@teste.com')
        self.assertEqual(mail.outbox[1].to, ['rennerocha@gmail.com'])

        self.assertRedirects(response, reverse('contribuicao-recebida'))
