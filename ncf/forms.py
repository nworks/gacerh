from django import forms

class fechaform(forms.Form):
    mes = forms.CharField(label='mes', max_length=10)
    ano = forms.CharField(label='ano', max_length=10)