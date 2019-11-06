from django.db import models

# Create your models here.
class Variavel(models.Model):
    nome = models.CharField(max_length=32)
    flObjetivo = models.BooleanField(default=False)

class Atributo(models.Model):
    nome = models.CharField(max_length=32)
    variavel = models.ForeignKey(Variavel, on_delete=models.CASCADE, related_name='atributos')
    inicioBase = models.IntegerField()
    fimBase = models.IntegerField()
    inicioNucleo = models.IntegerField()
    fimNucleo = models.IntegerField()

class Regra(models.Model):
    descricao = models.CharField(max_length=4000)