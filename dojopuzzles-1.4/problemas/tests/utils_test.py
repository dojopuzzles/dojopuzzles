# -*- coding: utf-8 -*-
from problemas.models import Problema


def novo_problema(dados_problema):
    """
    Cadastra um novo problema no sistema para ser utilizado
    em testes.
    """
    numero_problemas = Problema.objects.count()
    indice = numero_problemas + 1

    dados_problema.setdefault('titulo', "Título Problema Teste {0}".format(indice))
    dados_problema.setdefault('publicado', True)

    problema = Problema(**dados_problema)
    problema.save()

    return problema
