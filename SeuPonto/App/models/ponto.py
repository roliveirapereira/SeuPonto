from django.contrib.auth.models import User
from django.db import models

class Ponto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entrada = models.DateTimeField()
    saida = models.DateTimeField()
    carga_horaria = models.DurationField()
    descricao = models.TextField(max_length=100)
    
    def __str__(self):
        return f'{self.user.username} - {self.entrada} - {self.saida}'