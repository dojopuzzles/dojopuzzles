# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from problemas.models import ProblemaUtilizado
from problemas.tests.utils_test import novo_problema

ITEM_MAIS_UTILIZADO = u"%s (%s)"


class VisualizacaoProblemasMaisUtilizadosTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def teste_nenhum_problema_utilizado(self):
        """
        Se nenhum problema foi utilizado ainda
        não deve exibir o bloco de problemas mais
        utilizados.
        """
        response = self.client.get(reverse('inicio'))
        self.assertNotContains(response, u'MAIS UTILIZADOS')

    def teste_existe_problema_utilizado(self):
        """
        Se ao menos um problema tiver sido indicado como utilizado
        deve exibir o bloca de problemas utilizados.
        """
        problema = novo_problema({})
        problema.utilizar()

        response = self.client.get(reverse('inicio'))
        self.assertContains(response, u'MAIS UTILIZADOS', 1)

    def teste_exibe_problemas_utilizados_em_ordem_decrescente(self):
        """
        Os problemas utilizados devem ser exibidos em ordem decrescente de
        utilizações.
        """
        problema1 = novo_problema({})
        problema2 = novo_problema({})

        problema2.utilizar()
        problema2.utilizar()
        problema1.utilizar()

        response = self.client.get(reverse('inicio'))

        # Estou verificando desta maneira pois ainda não sei como testar o conteúdo do
        # contexto de uma templatetag
        # O título do problema2 (mais utilizado) deve aparecer antes do título do problema1 (menos utilizado)
        self.assertTrue(response.content.find(problema2.titulo) < response.content.find(problema1.titulo))

    def teste_problemas_mais_recentes(self):
        """
        Se dois problemas foram utilizados o mesmo número de vezes, o problema que foi utilizado mais
        recentemente deve aparecer antes na listagem.
        """
        problema1 = novo_problema({})
        problema2 = novo_problema({})

        problema2.utilizar()
        problema1.utilizar()
        problema2.utilizar()
        problema2.utilizar()
        problema1.utilizar()
        problema1.utilizar()

        response = self.client.get(reverse('inicio'))

        # Como o problema1 foi utilizado pela última vez, ele deve aparecer antes do problema2
        self.assertTrue(response.content.find(problema1.titulo) < response.content.find(problema2.titulo))

    def teste_so_exibe_os_5_ultimos_mais_utilizados(self):
        """
        Só devem ser exibidos os 5 últimos problemas mais utilizados.
        """
        problema1 = novo_problema({})
        problema2 = novo_problema({})
        problema3 = novo_problema({})
        problema4 = novo_problema({})
        problema5 = novo_problema({})
        problema6 = novo_problema({})

        problema1.utilizar()
        problema1.utilizar()
        problema1.utilizar()
        problema1.utilizar()

        problema2.utilizar()
        problema2.utilizar()
        problema2.utilizar()

        problema3.utilizar()
        problema3.utilizar()

        problema4.utilizar()
        problema4.utilizar()

        problema5.utilizar()
        problema5.utilizar()

        problema6.utilizar()
        problema6.utilizar()

        response = self.client.get(reverse('inicio'))

        self.assertNotContains(response, problema6.titulo)
        self.assertContains(response, problema1.titulo, 1)
        self.assertContains(response, problema2.titulo, 1)
        self.assertContains(response, problema3.titulo, 1)
        self.assertContains(response, problema4.titulo, 1)
        self.assertContains(response, problema5.titulo, 1)
