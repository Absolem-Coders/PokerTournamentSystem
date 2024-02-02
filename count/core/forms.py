# forms.py
from django import forms
from .models import Jogador

class JogadorForm(forms.ModelForm):

    class Meta:
        model = Jogador
        fields = ('nome', 'buy_in', 'rebuys', 'add_ons')
