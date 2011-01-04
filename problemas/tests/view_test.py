#:-*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from dojopuzzles.problemas.models import Problema, ProblemaUtilizado

class UrlsTestCase(TestCase):
    """ Testa as URLs da aplicação """
    def setUp(self):
        self.problema = Problema(titulo="Título do Problema 1",
                                 descricao="Descrição do Problema 1")
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

        response = self.client.get(reverse('todos-problemas'))
        self.assertNotEqual(response.status_code, 404)

class ExibicaoProblemaTestCase(TestCase):

    def setUp(self):
        # Cadastra 2 problemas que serão utilizados nos testes
        for i in xrange(1,3):
            titulo = "Título do Problema {0}".format(i)
            descricao = "Descrição do Problema {0}".format(i)
            problema = Problema(titulo=titulo, descricao=descricao)
            problema.save()
        self.client = Client()
        
    def tearDown(self):
        Problema.objects.all().delete()

    def test_visualizacao_de_problema(self):
        """ Se o usuário visualizar um problema, ao exibir outro problema, 
        o problema anterior deve estar na lista de problemas visualizados """
        problema_exibido1 = Problema.objects.all()[0]
        response = self.client.get(reverse('exibe-problema', args=[problema_exibido1.id]), follow=True)
        try:
            problemas_visualizados = self.client.session['problemas_visualizados']
            self.assertTrue(problema_exibido1 in problemas_visualizados)
        except KeyError:
            self.fail('Não existe lista de problemas visualizados.')
            
        problema_exibido2 = Problema.objects.all()[1]
        response = self.client.get(reverse('exibe-problema', args=[problema_exibido2.id]), follow=True)
        try:
            problemas_visualizados = self.client.session['problemas_visualizados']
            self.assertTrue(problema_exibido1 in problemas_visualizados)
            self.assertTrue(problema_exibido2 in problemas_visualizados)
        except KeyError:
            self.fail('Não existe lista de problemas visualizados.')

    def test_nao_repete_problema_visualizado(self):
        """ Não é permitido um problema estar na lista de problemas visualizados mais de uma vez """
        problema_exibido1 = Problema.objects.all()[0]

        response = self.client.get(reverse('exibe-problema', args=[problema_exibido1.id]), follow=True)
        problemas_visualizados = self.client.session['problemas_visualizados']
        self.assertEqual(problemas_visualizados.count(problema_exibido1), 1)

        response = self.client.get(reverse('exibe-problema', args=[problema_exibido1.id]), follow=True)
        problemas_visualizados = self.client.session['problemas_visualizados']
        self.assertEqual(problemas_visualizados.count(problema_exibido1), 1)

class ProblemaAleatorioTest(TestCase):

    def setUp(self):
        # Cadastra 10 problemas que serão utilizados nos testes
        for i in xrange(1,11):
            titulo = "Título do Problema {0}".format(i)
            descricao = "Descrição do Problema {0}".format(i)
            problema = Problema(titulo=titulo, descricao=descricao)
            problema.save()
        self.client = Client()

    def tearDown(self):
        Problema.objects.all().delete()

    def test_nenhum_problema_cadastrado(self):
        """ Se nenhum problema estiver cadastrado exibe página informando """
        Problema.objects.all().delete() # Apaga todos os problemas
        response = self.client.get(reverse('problema-aleatorio'))
        self.assertRedirects(response, reverse('nenhum-problema-cadastrado'))

    def test_retornando_problemas_aleatorios(self):
        """ Verificando se ao solicitar um problema aleatório o retorno é um problema
        ainda não visualizado ou a informação de que todos os problemas disponíveis
        já foram visualizados """
        numero_problemas = Problema.objects.count()
        for i in xrange(1, numero_problemas + 1):
            # Como temos 'numero_problemas' problemas de teste cadastrados, 
            # após 'numero_problemas' chamadas de problemas aleatórios, 
            # todos os problemas devem ser visualizados uma única vez
            response = self.client.get(reverse('problema-aleatorio'), follow=True)

        # Após exibir todos os problemas, uma solicitação de um problema 
        # aleatório deve informar que não existe mais nenhum problema novo 
        # cadastrado
        response = self.client.get(reverse('problema-aleatorio'), follow=True)
        self.assertEqual(len(self.client.session['problemas_visualizados']), numero_problemas)
        self.assertRedirects(response, reverse('sem-problemas-novos'))

class ProblemaNaoDesejadoTest(TestCase):

    def setUp(self):
        # Cadastra 5 problemas que serão utilizados nos testes
        for i in xrange(1,6):
            titulo = "Título do Problema {0}".format(i)
            descricao = "Descrição do Problema {0}".format(i)
            problema = Problema(titulo=titulo, descricao=descricao)
            problema.save()
        self.client = Client()

    def test_se_usuario_nao_gostar_do_problema(self):
        """ Se o usuário não gostar de um problema, ele não deve mais ser 
        exibido nos problemas aleatórios e nem na lista de problemas 
        visualizados """
        numero_problemas = Problema.objects.count()
        problema_nao_gostei = Problema.objects.all()[0]
        response = self.client.get(reverse('exibe-problema', args=[problema_nao_gostei.id]), follow=True)
        problemas_visualizados = self.client.session['problemas_visualizados']

        try:
            problemas_nao_gostei = self.client.session['problemas_nao_gostei']
            self.fail('A lista de problemas que eu não gostei não deve existir ainda.')
        except KeyError:
            pass

        self.assertTrue(problema_nao_gostei in problemas_visualizados)

        url_nao_gostei = "{0}?nao_gostei={1}".format(reverse('problema-aleatorio'), problema_nao_gostei.id)
        response = self.client.get(url_nao_gostei, follow=True)

        try:
            problemas_visualizados = self.client.session['problemas_visualizados']
            self.assertFalse(problema_nao_gostei in problemas_visualizados)
        except KeyError:
            self.fail('Problema que o usuário não gostou exibido na lista de problemas visualizados.')

        try:
            problemas_que_nao_gostei = self.client.session['problemas_que_nao_gostei']
            self.assertTrue(problema_nao_gostei in problemas_que_nao_gostei)
        except KeyError:
            self.fail('Problema que o usuário não gostou não está na lista de problemas recusados.')
            
class ProblemasGosteiTestCase(TestCase):

    def setUp(self):
        titulo = "Título do Problema 1"
        descricao = "Descrição do Problema 1"
        self.problema = Problema(titulo=titulo, descricao=descricao)
        self.problema.save()
        self.client = Client()
        
    def tearDown(self):
        Problema.objects.all().delete()
        ProblemaUtilizado.objects.all().delete()

    def test_problema_exibido_pela_primeira_vez(self):
        """ Um problema exibido pela primeira vez deve informar que nunca foi utilizado em um Dojo """
        response = self.client.get(reverse('exibe-problema', args=[self.problema.id]))
        self.assertContains(response, 'Este problema ainda não foi utilizado em nenhum Dojo.', 1)

    def test_problema_utilizado_em_um_dojo(self):
        """ Se alguém informar que gostou e vai utilizar um problema em um Dojo
        ao exibir este problema ele tem que informar quantas vezes ele já foi utilizado """

        url_gostei_e_vou_usar = "{0}?gostei".format(reverse('exibe-problema', args=[self.problema.id]))
        response = self.client.get(url_gostei_e_vou_usar)
        self.assertEqual(self.problema.utilizacoes, 1)
        self.assertContains(response, 'Este problema foi utilizado em 1 Dojo(s).', 1)
        self.assertContains(response, 'Você está resolvendo este problema.', 1)

        try:
            problema_utilizado = self.client.session['problema_utilizado']
            self.assertEqual(problema_utilizado, self.problema)
        except KeyError:
            self.fail('Problema que o usuário vai utilizar para o Dojo não está indicado.')

        # Se um novo usuário escolher este problema
        self.client.session.flush()
        url_gostei_e_vou_usar = "{0}?gostei".format(reverse('exibe-problema', args=[self.problema.id]))
        response = self.client.get(url_gostei_e_vou_usar)
        self.assertEqual(self.problema.utilizacoes, 2)
        self.assertContains(response, 'Este problema foi utilizado em 2 Dojo(s).', 1)
        
    def test_exibicao_problema_utilizado(self):
        """ Ao selecionar um problema para exibir não deve mais mostrar os botãoes de escolha """
        response = self.client.get(reverse('exibe-problema', args=[self.problema.id]))
        self.assertContains(response, 'id="botao_gostei"')
        self.assertContains(response, 'id="botao_talvez"')
        self.assertContains(response, 'id="botao_nao_gostei"')

        url_gostei_e_vou_usar = "{0}?gostei".format(reverse('exibe-problema', args=[self.problema.id]))
        response = self.client.get(url_gostei_e_vou_usar)
        self.assertNotContains(response, 'id="botao_gostei"')
        self.assertNotContains(response, 'id="botao_talvez"')
        self.assertNotContains(response, 'id="botao_nao_gostei"')        
