from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from App.models import Ponto, Pausa
from pytz import timezone
import json

@login_required
def home_view(request):
    ativo = False
    user = request.user
    ponto = Ponto.objects.filter(user=user).last()
    print(ponto)
    if ponto is not None:
        if ponto.saida is None:
            ativo = True
        else:
            ativo = False
    return render(request, 'home.html', {'user': user, 'ativo':ativo})  

@csrf_exempt
@login_required
@csrf_exempt
def registrar_ponto(request):
    if request.method == "POST":
        user = request.user
        ponto = Ponto.objects.create(user=user, entrada=now(), status="ativo")
        return JsonResponse({"message": "Ponto iniciado", "entrada": ponto.entrada.timestamp()})

@csrf_exempt
def finalizar_ponto(request):
    if request.method == "POST":
        data = json.loads(request.body)
        descricao = data.get("descricao", "")
        anotacao_tecnica = data.get("anotacao_tecnica", "")

        user = request.user
        ponto = Ponto.objects.filter(user=user, status="ativo").last()
        print(ponto)
        if ponto is not None:
            ponto.saida = now()
            ponto.carga_horaria = ponto.saida - ponto.entrada
            ponto.status = "finalizado"
            ponto.descricao = descricao
            ponto.anotacao_tecnica = anotacao_tecnica
            ponto.save()
            return JsonResponse({"message": "Ponto finalizado"})
        return JsonResponse({"error": "Nenhum ponto ativo encontrado"}, status=404)