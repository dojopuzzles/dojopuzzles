#:-*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from dojo.problemas.models import Problema

class UrlsTestCase(TestCase):
    """ Testa as URLs da aplicação """
    def setUp(self):
        titulo = "Título do Problema 1"
        descricao = "Descrição do Problema 1"
        self.problema = Problema(titulo=titulo, descricao=descricao)
        self.problema.save()
        self.client = Client()
            
    def test_existencia_urls(self):
        response = self.client.get(reverse('problema-aleatorio'))
        self.assertNotEqual(response.status_code, 404)
        
        response = self.client.get(reverse('exibe-problema', args=[self.problema.id]))
        self.assertNotEqual(response.status_code, 404)
        
        response = self.client.get(reverse('sem-problemas-novos'))
        self.assertNotEqual(response.status_code, 404)
        
        response = self.client.get(reverse('nenhum-problema-cadastrado'))
        self.assertNotEqual(response.status_code, 404)

class ProblemaAleatorioTest(TestCase):
    """ """
    
    def setUp(self):
        # Cadastra 10 problemas que serão utilizados nos testes
        for i in xrange(1,11):
            titulo = "Título do Problema {0}".format(i)
            descricao = "Descrição do Problema {0}".format(i)
            problema = Problema(titulo=titulo, descricao=descricao)
            problema.save()
        self.client = Client()
            
    def test_nenhum_problema_cadastrado(self):
        """ Se nenhum problema estiver cadastrado exibe o template correspondente """
        Problema.objects.all().delete() # Apaga todos os problemas da base de dados
        response = self.client.get(reverse('problema-aleatorio'))
        self.assertRedirects(response, reverse('nenhum-problema-cadastrado'))

    def test_retornando_problemas_aleatorios(self):
        """ Verificando se ao solicitar um problema aleatório o retorno é um problema
        ainda não visualizado ou a informação de que todos os problemas disponíveis
        já foram visualizados """
        problemas_visualizados = []
        numero_problemas = Problema.objects.count()
        for i in xrange(1, numero_problemas + 1):
            # Como temos 'numero_problemas' problemas de teste cadastrados, 
            # após 'numero_problemas' chamadas de problemas aleatórios, 
            # todos os problemas devem ser visualizados uma única vez
            response = self.client.get(reverse('problema-aleatorio'))
            problema_visualizado = response['Location']
            if problema_visualizado in problemas_visualizados:
                self.fail('Reexibindo problema já visualizado')
            problemas_visualizados.append(response['Location'])

        # Após exibir todos os problemas, uma solicitação de um problema 
        # aleatório deve informar que não existe mais nenhum problema novo 
        # cadastrado
        response = self.client.get(reverse('problema-aleatorio'))
        self.assertRedirects(response, reverse('sem-problemas-novos'))


