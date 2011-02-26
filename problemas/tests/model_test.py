# -*- coding: utf-8 -*-
from django.test import TestCase

from dojopuzzles.problemas.models import Problema


class CriacaoProblemaTestCase(TestCase):

    def test_problema_inicia_nao_publicado(self):
        """
        Um problema quando é cadastrado é definido como não publicado
        """
        problema = Problema(titulo=u'Problema Não Publicado Teste 1',
                            descricao=u'Descrição do Problema Não Publicado')
        self.assertFalse(problema.publicado)
