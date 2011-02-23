# -*- coding: utf-8 -*-
from django import forms

ASSUNTO_CHOICES = (
    ('', '---------'),
    ('PROBLEMA_NOVO', u'Envio de novo problema'),
    ('CONTATO', 'Quero entrar em contato com a equipe'),
)

class ContribuicaoForm(forms.Form):
    """ Formulário que recebe as contribuições para o projeto """
    nome = forms.CharField(max_length=100, label='Seu Nome')
    email = forms.EmailField(label='Seu e-mail')
    assunto = forms.ChoiceField(label='Assunto',
                                choices=ASSUNTO_CHOICES)
    mensagem = forms.CharField(label='Sua Mensagem', widget=forms.widgets.Textarea(attrs={'rows':15, 'cols':60}))
