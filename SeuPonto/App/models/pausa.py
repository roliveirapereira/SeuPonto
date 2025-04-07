from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class Pausa(models.Model):
    inicio = models.DateTimeField(auto_now_add=True)
    fim = models.DateTimeField(null=True, blank=True)
    ponto = models.ForeignKey('Ponto', on_delete=models.CASCADE, related_name='pausas')
    status = models.CharField(max_length=10, default='ativo')
    
    @property
    def duracao(self):
        if self.fim:
            return self.fim - self.inicio
        return now() - self.inicio
    def __str__(self):
        return f'{self.inicio} - {self.fim or "Em pausa"}'
    