from django.db import models

# Create your models here.
class Problema(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()

    def __unicode__(self):
        return self.titulo
