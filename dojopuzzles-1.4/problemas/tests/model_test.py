# -*- coding: utf-8 -*-
from django.test import TestCase

from problemas.models import Problema
from problemas.tests.utils_test import novo_problema


class ProblemasTestCase(TestCase):

    def test_problema_inicia_nao_publicado(self):
        """
        Um problema quando é cadastrado é definido como não publicado
        """
        problema = Problema(titulo=u'Problema Não Publicado Teste 1',
                            descricao=u'Descrição do Problema Não Publicado')
        self.assertFalse(problema.publicado)

    def test_utilizar_problema_aumenta_numero_utilizacoes(self):
        """
        Se utilizarmos um problema, o contador de utilizações deve ser incrementado
        """
        problema = novo_problema({})
        self.assertEqual(problema.utilizacoes, 0)
        problema.utilizar()
        self.assertEqual(problema.utilizacoes, 1)

    def test_somente_problemas_publicados_podem_ser_utilizados(self):
        """
        Somente problemas publicados podem ser utilizados.
        """
        problema = novo_problema({'publicado': False})
        problema.utilizar()
        self.assertRaises(Exception, problema.utilizar())
