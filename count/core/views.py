# views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Jogador
from .serializers import JogadorSerializer
from django.db.models import Sum
from .models import Level
from .serializers import LevelSerializer
from django.utils import timezone
from datetime import timedelta
from .prices import buyin, buyin_preco, rebuy, rebuy_preco, addon, addon_preco

@api_view(['GET'])
def jogador_list(request):
    jogadores = Jogador.objects.all()
    serializer = JogadorSerializer(jogadores, many=True)
    return Response({
        'jogadores': serializer.data,
    })

@api_view(['GET'])
def jogador_detail(request, pk):
    jogador = get_object_or_404(Jogador, pk=pk)
    serializer = JogadorSerializer(jogador)
    return Response(serializer.data)

@api_view(['POST'])
def jogador_novo(request):
    serializer = JogadorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def jogador_editar(request, pk):
    jogador = get_object_or_404(Jogador, pk=pk)
    serializer = JogadorSerializer(jogador, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def jogador_excluir(request, pk):
    jogador = get_object_or_404(Jogador, pk=pk)
    jogador.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def total_premio(request):
    total_premio_by = Jogador.objects.aggregate(Sum('buy_in'))['buy_in__sum'] or 0
    total_premio_rb = Jogador.objects.aggregate(Sum('rebuys'))['rebuys__sum'] or 0
    total_premio_ad = Jogador.objects.aggregate(Sum('add_ons'))['add_ons__sum'] or 0
    
    total_premio_by_valor = total_premio_by * buyin_preco
    total_premio_rb_valor = total_premio_rb * rebuy_preco
    total_premio_ad_valor = total_premio_ad * addon_preco
    total = total_premio_by_valor + total_premio_rb_valor + total_premio_ad_valor

    return Response({
        'qtd_buyins': total_premio_by, 
        'qtd_rebuys': total_premio_rb,
        'qtd_addons': total_premio_ad,
        'vlr_buyins': total_premio_by_valor,
        'vlr_rebuys': total_premio_rb_valor,
        'vlr_addons': total_premio_ad_valor,
        'valor_total': total,
                     })
    


@api_view(['GET'])
def get_level(request, nivel):
    try:
        level = Level.objects.get(nivel=nivel)
        serializer = LevelSerializer(level)
        return Response(serializer.data)
    except Level.DoesNotExist:
        return Response({'error': f'Nível {nivel} não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    
from .models import Torneio
from .serializers import TorneioSerializer

@api_view(['GET', 'POST'])
def torneio_list(request):
    if request.method == 'GET':
        torneios = Torneio.objects.all()
        serializer = TorneioSerializer(torneios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TorneioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def torneio_detail(request, torneio_id):
    try:
        torneio = Torneio.objects.get(id=torneio_id)
    except Torneio.DoesNotExist:
        return Response({'error': f'Torneio {torneio_id} não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TorneioSerializer(torneio)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TorneioSerializer(torneio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        torneio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def cair_jogador(request, torneio_id):
    try:
        torneio = Torneio.objects.get(id=torneio_id)
    except Torneio.DoesNotExist:
        return Response({'error': f'Torneio {torneio_id} não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    torneio.cair_jogador()
    serializer = TorneioSerializer(torneio)
    return Response(serializer.data)

@api_view(['POST'])
def add_jogador(request, torneio_id):
    try:
        torneio = Torneio.objects.get(id=torneio_id)
    except Torneio.DoesNotExist:
        return Response({'error': f'Torneio {torneio_id} não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    torneio.add_jogador()
    serializer = TorneioSerializer(torneio)
    return Response(serializer.data)

@api_view(['GET'])
def calcular_chips(request, torneio_id):
    try:
        torneio = Torneio.objects.get(id=torneio_id)
    except Torneio.DoesNotExist:
        return Response({'error': f'Torneio {torneio_id} não encontrado.'}, status=404)

    # Calcular os totais de buy-ins, rebuys e addons
    total_premio_by = Jogador.objects.aggregate(Sum('buy_in'))['buy_in__sum'] or 0
    total_premio_rb = Jogador.objects.aggregate(Sum('rebuys'))['rebuys__sum'] or 0
    total_premio_ad = Jogador.objects.aggregate(Sum('add_ons'))['add_ons__sum'] or 0
    totalbonus = Jogador.objects.aggregate(Sum('fichasbonus'))['fichasbonus__sum'] or 0

    # Calcular o valor total de fichas no torneio
    total_fichas = (total_premio_by * buyin) + (total_premio_ad * addon) + (total_premio_rb * rebuy) + totalbonus

    # Calcular o stack médio
    if torneio.jogadores_atual > 0:
        stack_medio = total_fichas / torneio.jogadores_atual
    else:
        stack_medio = 0

    return Response({
        'total_fichas': total_fichas,
        'stack_medio': stack_medio,
    })
    

@api_view(['GET'])
def nivel_atual(request, torneio_id):
    torneio = get_object_or_404(Torneio, id=torneio_id)

    tempo_decorrido = timezone.now() - torneio.horario_inicio
    minutos_decorridos = tempo_decorrido.total_seconds() / 60
        
    # Calcular o número do nível com base no tempo decorrido e na duração de cada nível
    if torneio.intervalo_ativo:
        duracao_nivel = torneio.tempo_blind_posintervalo  # Duração do nível após o intervalo
        minutosposintervalo = timezone.now() - torneio.horario_intervalo
        minutosposintervalo = round(minutosposintervalo.total_seconds() / 60)
        
        niveisantes = torneio.horario_intervalo - torneio.horario_inicio
        niveisantes = round(niveisantes.total_seconds() / 60)
        
        # Calcular quantos níveis aconteceram desde o início do torneio até o intervalo com o blind pré-intervalo
        niveis_antes_intervalo = round(int(niveisantes / torneio.tempo_blind_preintervalo))
        # Calcular o número do nível considerando o tempo decorrido após o intervalo, desconsiderando o tempo de intervalo
        numero_nivel = round(niveis_antes_intervalo + int(minutosposintervalo / duracao_nivel))
        if numero_nivel == 0:
            numero_nivel = 1
        print(niveisantes, niveis_antes_intervalo, minutosposintervalo, duracao_nivel)
    else:
        duracao_nivel = torneio.tempo_blind_preintervalo  # Duração do nível antes do intervalo
        numero_nivel = round(int(minutos_decorridos / duracao_nivel) + 1)
        if numero_nivel == 0:
            numero_nivel = 1
    
    
    # Obter o nível correspondente ao número calculado
    try:
        nivel = Level.objects.get(nivel=numero_nivel)
    except Level.DoesNotExist:
        return Response({'mensagem': 'Torneio em andamento, mas nível não encontrado.', "nivel": numero_nivel}, status=200)

    return Response({
        'numero_nivel': numero_nivel,
        'nivel_atual': str(nivel),
    })
    
@api_view(['POST'])
def comecar_torneio(request, torneio_id):
    torneio = get_object_or_404(Torneio, id=torneio_id)
    torneio.comecar_torneio()
    return Response({'message': f'Torneio {torneio_id} começou com sucesso!'})

@api_view(['POST'])
def ativar_intervalo(request, torneio_id):
    try:
        torneio = Torneio.objects.get(id=torneio_id)
    except Torneio.DoesNotExist:
        return Response({'error': f'Torneio {torneio_id} não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    torneio.intervalo_ativo = True
    torneio.save()

    return Response({'message': 'Intervalo ativado com sucesso!'})
