# serializers.py
from rest_framework import serializers
from .models import Jogador
from .models import Level
from .models import Torneio

class JogadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jogador
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'
        


class TorneioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneio
        fields = '__all__'