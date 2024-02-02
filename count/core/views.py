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
    
    total_premio_by_valor = total_premio_by * 30
    total_premio_rb_valor = total_premio_rb * 30
    total_premio_ad_valor = total_premio_ad * 70
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