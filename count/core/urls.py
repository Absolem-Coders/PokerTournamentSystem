# urls.py
from django.urls import path
from .views import (
    jogador_list,
    jogador_detail,
    jogador_novo,
    jogador_editar,
    jogador_excluir,
    total_premio,
    get_level,
    torneio_list,
    torneio_detail,
    cair_jogador,
    add_jogador,
    calcular_chips,
    nivel_atual,
    comecar_torneio,
    ativar_intervalo
)

urlpatterns = [
    path('api/jogadores/', jogador_list, name='api_jogador_list'),
    path('api/jogador/<int:pk>/', jogador_detail, name='api_jogador_detail'),
    path('api/jogador/novo/', jogador_novo, name='api_jogador_novo'),
    path('api/jogador/<int:pk>/editar/', jogador_editar, name='api_jogador_editar'),
    path('api/jogador/<int:pk>/excluir/', jogador_excluir, name='api_jogador_excluir'),
    path('api/total_premio/', total_premio, name='api_total_premio'), 
    path('api/level/<int:nivel>/', get_level, name='get_level'),
    path('api/torneios/', torneio_list, name='torneio_list'),
    path('api/torneio/<int:torneio_id>/', torneio_detail, name='torneio_detail'),
    path('api/cair_jogador/<int:torneio_id>/', cair_jogador, name='cair_jogador'),
    path('api/add_jogador/<int:torneio_id>/', add_jogador, name='add_jogador'),
    path('api/torneio/<int:torneio_id>/chips/', calcular_chips, name='calcular_chips'),
    path('api/torneio/<int:torneio_id>/nivel_atual/', nivel_atual, name='nivel_atual'),
    path('api/comecar_torneio/<int:torneio_id>/', comecar_torneio, name='comecar_torneio'),
    path('ativar_intervalo/<int:torneio_id>/', ativar_intervalo, name='ativar_intervalo'),
]
