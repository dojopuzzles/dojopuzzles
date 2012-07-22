# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import signals
from django.template.defaultfilters import slugify


class Problema(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    descricao = models.TextField()
    nome_contribuidor = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=False, unique=True)
    publicado = models.BooleanField(default=False)

    def __unicode__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('exibe-problema', kwargs={'slug': self.slug})

    def _get_utilizacoes(self):
        return ProblemaUtilizado.objects.filter(problema=self).count()
    utilizacoes = property(_get_utilizacoes)

    def utilizar(self):
        """
        Informa que o problema foi utilizado em um Dojo.
        """
        utilizado = ProblemaUtilizado(problema=self)
        utilizado.save()


class ProblemaUtilizado(models.Model):
    problema = models.ForeignKey(Problema)
    data_utilizacao = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Problema utilizado: %s" % (self.problema.titulo, )


class SolucaoProblema(models.Model):
    problema = models.ForeignKey(Problema)
    solucao = models.URLField()


def problema_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.titulo)

signals.pre_save.connect(problema_pre_save, sender=Problema)
