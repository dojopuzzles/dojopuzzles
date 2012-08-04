# -*- coding: utf-8 -*-
from django.contrib import admin
from problemas.models import Problema, ProblemaUtilizado


class ProblemaAdmin(admin.ModelAdmin):
    list_filter = ('publicado',)


class ProblemaUtilizadoAdmin(admin.ModelAdmin):
    list_display = ('problema', 'data_utilizacao')

admin.site.register(Problema, ProblemaAdmin)
admin.site.register(ProblemaUtilizado, ProblemaUtilizadoAdmin)
