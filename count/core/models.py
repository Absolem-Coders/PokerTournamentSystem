from django.db import models
from django.utils import timezone

# Create your models here.
class Jogador(models.Model):
    nome = models.CharField(max_length=100)
    buy_in = models.IntegerField(default=1)
    rebuys = models.IntegerField(default=0)
    add_ons = models.IntegerField(default=0)
    def __str__(self):
        return self.nome
    

class Level(models.Model):
    nivel = models.IntegerField(unique=True)
    small = models.IntegerField()
    big = models.IntegerField()

    def __str__(self):
        return f'Nível {self.nivel}'

class Torneio(models.Model):
    nome_torneio = models.CharField(max_length=100)
    jogadores_total = models.IntegerField()
    jogadores_atual = models.IntegerField()
    horario_inicio = models.DateTimeField(default=timezone.now)
    horario_intervalo = models.DateTimeField()
    buyin_valor = models.IntegerField()
    rebuy_valor = models.IntegerField()
    addon_valor = models.IntegerField()

    def __str__(self):
        return f'Torneio {self.id}'
    
    def cair_jogador(self):
        if self.jogadores_atual > 0:
            self.jogadores_atual -= 1
            self.save()
    def add_jogador(self):
        self.jogadores_atual += 1
        self.save()
    def comecar_torneio(self):
        self.horario_inicio = timezone.now()
        self.save()