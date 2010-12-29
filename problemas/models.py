from django.db import models

# Create your models here.
class Problema(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()

    def __unicode__(self):
        return self.titulo

    def _get_utilizacoes(self):
        return ProblemaUtilizado.objects.filter(problema=self).count()
    utilizacoes = property(_get_utilizacoes)

class ProblemaUtilizado(models.Model):
    problema = models.ForeignKey(Problema)
    data_utilizacao = models.DateField(auto_now_add=True)
