# -*- coding: utf-8 -*-
from django.contrib import admin
from dojopuzzles.problemas.models import Problema, ProblemaUtilizado

class ProblemaUtilizadoAdmin(admin.ModelAdmin):
    list_display = ('problema', 'data_utilizacao')

admin.site.register(Problema)
admin.site.register(ProblemaUtilizado, ProblemaUtilizadoAdmin)
