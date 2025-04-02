from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta
from django.utils.timezone import now

class Ponto(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('pausado', 'Pausado'),
        ('finalizado', 'Finalizado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entrada = models.DateTimeField(auto_now_add=True)
    saida = models.DateTimeField(null=True, blank=True)
    carga_horaria = models.DurationField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    descricao = models.TextField(max_length=100)
    tempo_pausado = models.DurationField(default=timedelta(0))
    ultimo_pausa = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.entrada} - {self.saida or "Em andamento"}'