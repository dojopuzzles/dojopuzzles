#-*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from problemas.models import Problema, ProblemaUtilizado, SolucaoProblema
from problemas.tests.utils_test import novo_problema


#FIXME Esta classe de teste não deveria ficar aqui
class CoreTestCase(TestCase):
    """ Testes não relacionados a nenhuma aplicação """

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        ProblemaUtilizado.objects.all().delete()
        Problema.objects.all().delete()

    def test_nenhum_problema_utilizado(self):
        """
        Se nenhum problema foi utilizado ainda, não deve exibir nenhuma
        informação referente a problemas utilizados.
        """
        problema1 = novo_problema({})
        problema2 = novo_problema({})
        client = Client()
        response = client.get(reverse('inicio'))
        self.assertNotContains(response, u"Os problemas deste site já foram utilizados")

    def test_exibe_numero_problemas_utilizados(self):
        """
        Deve exibir na página inicial a quantidade de vezes que
        algum problema foi utilizado em um Coding Dojo
        """
        problema1 = novo_problema({})
        problema2 = novo_problema({})

        contador = 0
        for utilizacao in range(1, 11):
            problema1.utilizar()
            problema2.utilizar()
            contador += 1

        response = self.client.get(reverse('inicio'))
        self.assertContains(response, u"Os problemas deste site já foram utilizados em 20 Coding Dojos!!!", 1)

        problema2.utilizar()
        response = self.client.get(reverse('inicio'))
        self.assertContains(response, u"Os problemas deste site já foram utilizados em 21 Coding Dojos!!!", 1)


class UrlsTestCase(TestCase):
    """ Testa as URLs da aplicação """
    def setUp(self):
        self.problema = novo_problema({})
        self.client = Client()

    def test_existencia_urls(self):
        response = self.client.get(reverse('problema-aleatorio'))
        self.assertNotEqual(response.status_code, 404)

        response = self.client.get(reverse('exibe-problema', args=[self.problema.slug]))
        self.assertNotEqual(response.status_code, 404)
        titulo = "<title>DojoPuzzles.com - {0}</title>"
        self.assertContains(response, titulo.format(self.problema.titulo), 1)

        response = self.client.get(reverse('exibe-problema-pelo-id', args=[self.problema.id]))
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(response['Location'], 'http://testserver{0}'.format(reverse('exibe-problema', args=[self.problema.slug])))

        response = self.client.get(reverse('sem-problemas-novos'))
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, "<title>DojoPuzzles.com - Todos os problemas visualizados</title>", 1)

        response = self.client.get(reverse('nenhum-problema-cadastrado'))
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, "<title>DojoPuzzles.com - Nenhum problema cadastrado</title>", 1)

        response = self.client.get(reverse('todos-problemas'))
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, "<title>DojoPuzzles.com - Problemas cadastrados</title>", 1)

        response = self.client.get(reverse('problema-utilizado-em-dojo', args=[self.problema.id]), follow=True)
        self.assertNotEqual(response.status_code, 404)
        titulo = "<title>DojoPuzzles.com - {0}</title>"
        self.assertContains(response, titulo.format(self.problema.titulo), 1)


class ExibicaoProblemaTestCase(TestCase):

    def setUp(self):
        # Cadastra 2 problemas que serão utilizados nos testes
        for i in xrange(1, 3):
            novo_problema({})
        self.client = Client()

    def tearDown(self):
        Problema.objects.all().delete()

    def test_visualizacao_de_problema(self):
        """ Se o usuário visualizar um problema, ao exibir outro problema,
        o problema anterior deve estar na lista de problemas visualizados """
        problema_exibido1 = Problema.objects.all()[0]
        response = self.client.get(reverse('exibe-problema', args=[problema_exibido1.slug]), follow=True)
        try:
            problemas_visualizados = self.client.session['problemas_visualizados']
            self.assertTrue(problema_exibido1 in problemas_visualizados)
        except KeyError:
            self.fail('Não existe lista de problemas visualizados.')

        problema_exibido2 = Problema.objects.all()[1]
        response = self.client.get(reverse('exibe-problema', args=[problema_exibido2.slug]), follow=True)
        try:
            problemas_visualizados = self.client.session['problemas_visualizados']
            self.assertTrue(problema_exibido1 in problemas_visualizados)
            self.assertTrue(problema_exibido2 in problemas_visualizados)
        except KeyError:
            self.fail('Não existe lista de problemas visualizados.')

    def test_nao_repete_problema_visualizado(self):
        """ Não é permitido um problema estar na lista de problemas visualizados mais de uma vez """
        problema_exibido1 = Problema.objects.all()[0]

        response = self.client.get(reverse('exibe-problema', args=[problema_exibido1.slug]), follow=True)
        problemas_visualizados = self.client.session['problemas_visualizados']
        self.assertEqual(problemas_visualizados.count(problema_exibido1), 1)

        response = self.client.get(reverse('exibe-problema', args=[problema_exibido1.slug]), follow=True)
        problemas_visualizados = self.client.session['problemas_visualizados']
        self.assertEqual(problemas_visualizados.count(problema_exibido1), 1)

    def test_problema_sem_contribuidor_nao_exibe_nome(self):
        """ Um problema onde o contribuidor não é indicado, não deve exibir o título 'Contribuição de:' """
        problema = novo_problema({})
        response = self.client.get(reverse('exibe-problema', args=[problema.slug]), follow=True)
        self.assertNotContains(response, 'Contribuição de:')

    def test_problema_com_contribuidor_exibe_nome(self):
        """ Um problema onde o contribuidor é indicado, deve exibir o título 'Contribuição de: nome_contribuidor' """
        problema = novo_problema({'nome_contribuidor': 'Eu Que Contribui'})
        response = self.client.get(reverse('exibe-problema', args=[problema.slug]), follow=True)
        self.assertContains(response, 'Contribuição de: Eu Que Contribui', 1)

    def test_nao_exibe_problema_nao_publicado(self):
        """
        Um problema não publicado não pode ser exibido para o usuário
        """
        problema = novo_problema({'publicado': False})
        response = self.client.get(reverse('exibe-problema', args=[problema.slug]))
        self.assertTemplateUsed(response, '404.html')

    def test_nao_exibe_solucao_se_nao_tiver_nenhuma(self):
        """
        Ao exibir um problema, o botão que exibe as soluções que já estão cadastradas
        não deve ser exibido, caso o problema não tenha nenhuma solução.
        """
        problema = novo_problema({})
        response = self.client.get(reverse('exibe-problema', args=[problema.slug]))
        self.assertNotContains(response, 'id="botao_veja_solucoes"')

    def test_exibe_solucao_se_tiver_alguma(self):
        """
        Ao exibir um problema, o botão que exibe as soluções que já estão cadastradas
        não deve ser exibido, caso o problema não tenha nenhuma solução.
        """
        problema = novo_problema({})
        solucao = SolucaoProblema(problema=problema, solucao='http://teste.com/solucao')
        solucao.save()
        response = self.client.get(reverse('exibe-problema', args=[problema.slug]))
        self.assertContains(response, 'id="botao_veja_solucoes"')


class ProblemaAleatorioTest(TestCase):

    def setUp(self):
        # Cadastra 10 problemas que serão utilizados nos testes
        for i in xrange(1, 11):
            novo_problema({})
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

    def test_nao_deve_exibir_nao_publicado_como_aleatorio(self):
        """
        Ao solicitar um problema aleatório não deve exibir os problemas não publicados
        """
        Problema.objects.all().delete()
        problema_publicado = novo_problema({'publicado': True})
        problema_nao_publicado = novo_problema({'publicado': False})
        response = self.client.get(reverse('problema-aleatorio'), follow=True)
        titulo = "<title>DojoPuzzles.com - {0}</title>"
        self.assertContains(response, titulo.format(problema_publicado.titulo), 1)

        response = self.client.get(reverse('problema-aleatorio'), follow=True)
        self.assertRedirects(response, reverse('sem-problemas-novos'))


class ProblemaNaoDesejadoTest(TestCase):

    def setUp(self):
        # Cadastra 5 problemas que serão utilizados nos testes
        for i in xrange(1, 6):
            novo_problema({})
        self.client = Client()

    def test_se_usuario_nao_gostar_do_problema(self):
        """ Se o usuário não gostar de um problema, ele não deve mais ser
        exibido nos problemas aleatórios e nem na lista de problemas
        visualizados """
        numero_problemas = Problema.objects.count()
        problema_nao_gostei = Problema.objects.all()[0]
        response = self.client.get(reverse('exibe-problema', args=[problema_nao_gostei.slug]), follow=True)
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

    def test_informando_que_nao_gostou_do_mesmo_problema_de_novo(self):
        """ Se por algum motivo, forem feitas duas requisições informando que um problema não foi desejado
        deve ignorar o fato e simplesmente abrir um novo problema aleatório """
        problema_nao_gostei = Problema.objects.all()[0]
        url_nao_gostei = "{0}?nao_gostei={1}".format(reverse('problema-aleatorio'), problema_nao_gostei.id)
        response = self.client.get(url_nao_gostei, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url_nao_gostei, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_lista_de_nao_gostei_nao_tem_problemas_duplicados(self):
        problema_nao_gostei = Problema.objects.all()[0]
        url_nao_gostei = "{0}?nao_gostei={1}".format(reverse('problema-aleatorio'), problema_nao_gostei.id)
        response = self.client.get(url_nao_gostei, follow=True)
        response = self.client.get(url_nao_gostei, follow=True)
        self.assertEqual(self.client.session['problemas_que_nao_gostei'], [problema_nao_gostei])


class ProblemasGosteiTestCase(TestCase):

    def setUp(self):
        self.problema = novo_problema({})
        self.client = Client()

    def tearDown(self):
        Problema.objects.all().delete()
        ProblemaUtilizado.objects.all().delete()

    def test_problema_exibido_pela_primeira_vez(self):
        """ Um problema exibido pela primeira vez deve informar que nunca foi utilizado em um Dojo """
        response = self.client.get(reverse('exibe-problema', args=[self.problema.slug]))
        self.assertContains(response, 'Este problema ainda não foi utilizado em nenhum Dojo.', 1)

    def test_problema_utilizado_em_um_dojo(self):
        """ Se alguém informar que gostou e vai utilizar um problema em um Dojo
        ao exibir este problema ele tem que informar quantas vezes ele já foi utilizado """
        url_gostei_e_vou_usar = reverse('problema-utilizado-em-dojo', args=[self.problema.id])
        response = self.client.get(url_gostei_e_vou_usar, follow=True)
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
        url_gostei_e_vou_usar = reverse('problema-utilizado-em-dojo', args=[self.problema.id])
        response = self.client.get(url_gostei_e_vou_usar, follow=True)
        self.assertEqual(self.problema.utilizacoes, 2)
        self.assertContains(response, 'Este problema foi utilizado em 2 Dojo(s).', 1)

    def test_exibicao_problema_utilizado(self):
        """ Ao selecionar um problema para exibir não deve mais mostrar os botões de escolha """
        response = self.client.get(reverse('exibe-problema', args=[self.problema.slug]), follow=True)
        self.assertContains(response, 'id="botao_gostei"')
        self.assertContains(response, 'id="botao_talvez"')
        self.assertContains(response, 'id="botao_nao_gostei"')

        url_gostei_e_vou_usar = reverse('problema-utilizado-em-dojo', args=[self.problema.id])
        response = self.client.get(url_gostei_e_vou_usar, follow=True)
        self.assertNotContains(response, 'id="botao_gostei"')
        self.assertNotContains(response, 'id="botao_talvez"')
        self.assertNotContains(response, 'id="botao_nao_gostei"')

    def test_pagina_404(self):
        response = self.client.get(reverse('exibe-problema', args=['lala']))
        self.assertTemplateUsed(response, '404.html')


class ListagemProblemasTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_listagem_exibe_so_publicados(self):
        """
        A listagem de problemas deve exibir somente os problemas publicados.
        """
        problema1 = novo_problema({'publicado': False})
        problema2 = novo_problema({'publicado': True})

        response = self.client.get(reverse('todos-problemas'))

        self.assertNotContains(response, problema1.titulo)
        self.assertContains(response, problema2.titulo, 1)


class BuscaProblemaTestCase(TestCase):

    def tearDown(self):
        Problema.objects.all().delete()

    def test_buscando_com_palavra_chave_unica(self):
        """ Ao buscar um problema utilizando uma palavra chave que só exista
        em um único problema cadastrado deve redirecionar diretamente para ele """
        problema_unico = novo_problema({'titulo': u'Teste de Busca de Problema Único'})
        dados_busca = {'titulo': 'Único'}
        response = self.client.post(reverse('busca-problema-por-titulo'), dados_busca)
        self.assertRedirects(response, reverse('exibe-problema', args=[problema_unico.slug]))

    def test_buscando_problema_nao_publicado(self):
        """ Ao buscar um problema utilizando uma palavra chave que só exista
        em um único problema cadastrado mas não publicado deve informar que a busca
        não retornou nenhum registro """
        problema_nao_publicado = novo_problema({'titulo': u'Teste de Busca de Problema Não Publicado', 'publicado': False})
        dados_busca = {'titulo': 'não publicado'}
        response = self.client.post(reverse('busca-problema-por-titulo'), dados_busca)
        self.assertContains(response, "Nenhum problema encontrado contendo 'não publicado' em seu título.")

    def test_buscando_com_palavra_chave_repetida(self):
        """ Ao buscar um problema utilizando uma palavra chave que exista
        em mais de problema cadastrado deve exibir a lista de problemas encontrado """
        problema1 = novo_problema({'titulo': 'Título de Problema Repetido'})
        problema2 = novo_problema({'titulo': 'Outro Título Com Palavra Repetido'})
        dados_busca = {'titulo': 'repetido'}
        response = self.client.post(reverse('busca-problema-por-titulo'), dados_busca)
        self.assertContains(response, problema1.titulo)
        self.assertContains(response, problema2.titulo)

    def test_buscando_problema_inexistente(self):
        """ Ao buscar um problema utilizando uma palavra chave que não exista
        em nenhum problema cadastrado deve informar que a busca não retornou nenhum registro """
        dados_busca = {'titulo': 'não existe'}
        response = self.client.post(reverse('busca-problema-por-titulo'), dados_busca)
        self.assertContains(response, "Nenhum problema encontrado contendo 'não existe' em seu título.")

    def test_busca_vazia(self):
        """ Se nenhum parâmetro de busca for passado deve retornar listagem com todos os
        problemas cadastrados. """
        dados_busca = {'titulo': ''}
        response = self.client.post(reverse('busca-problema-por-titulo'), dados_busca)
        self.assertRedirects(response, reverse('todos-problemas'))

        dados_busca = {'titulo': ' '}
        response = self.client.post(reverse('busca-problema-por-titulo'), dados_busca)
        self.assertRedirects(response, reverse('todos-problemas'))
