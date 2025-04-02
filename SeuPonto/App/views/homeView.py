from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from App.models import Ponto

@login_required
def home_view(request):
    user = request.user
    return render(request, 'home.html', {'user': user})  

@csrf_exempt
@login_required
def registrar_ponto(request):
    user = request.user

    if request.method == "POST":
        action = request.POST.get("action")
        ponto = Ponto.objects.filter(user=user, saida__isnull=True).last()

        if action == "iniciar":
            # Criar um novo ponto ao iniciar
            ponto = Ponto.objects.create(
                user=user,
                entrada=now(),
                descricao="Ponto iniciado"
            )
            return JsonResponse({
                "status": "iniciado",
                "entrada": ponto.entrada.strftime('%Y-%m-%d %H:%M:%S')
            })

        elif action == "pausar":
            if ponto and ponto.ultimo_pausa is None:  # Apenas pausa se não já estiver pausado
                ponto.ultimo_pausa = now()
                ponto.save()
                return JsonResponse({"status": "pausado"})

        elif action == "continuar":
            if ponto and ponto.ultimo_pausa:
                tempo_pausa = now() - ponto.ultimo_pausa  # Calcula o tempo pausado
                ponto.tempo_pausado += tempo_pausa
                ponto.ultimo_pausa = None  # Reseta o último pausa
                ponto.save()
                return JsonResponse({"status": "continuado"})

        elif action == "finalizar":
            if ponto:
                ponto.saida = now()
                ponto.carga_horaria = (ponto.saida - ponto.entrada) - ponto.tempo_pausado  # Corrige carga horária
                ponto.save()
                return JsonResponse({
                    "status": "finalizado",
                    "entrada": ponto.entrada.strftime('%Y-%m-%d %H:%M:%S'),
                    "saida": ponto.saida.strftime('%Y-%m-%d %H:%M:%S'),
                    "carga_horaria": str(ponto.carga_horaria)
                })

        elif action == "cancelar":
            if ponto:
                ponto.delete()
                return JsonResponse({"status": "cancelado"})

    return JsonResponse({"error": "Método inválido"}, status=400)
