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
    titulo_problema = forms.CharField(max_length=100, label=u'Título do Problema', required=False)
    mensagem = forms.CharField(label='Sua Mensagem', widget=forms.widgets.Textarea(attrs={'rows': 15, 'cols': 60}))

    def clean(self):
        cleaned_data = self.cleaned_data

        assunto = cleaned_data.get('assunto')
        titulo_problema = cleaned_data.get('titulo_problema')

        if assunto == 'PROBLEMA_NOVO' and len(titulo_problema) == 0:
            raise forms.ValidationError(u"Informe o título do problema.")

        return cleaned_data
