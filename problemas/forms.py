# -*- coding: utf-8 -*-

from django import forms


class FormBusca(forms.Form):
    titulo = forms.CharField(max_length=100)
