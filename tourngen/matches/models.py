from django.db import models
from tournament_creator.models import Team
# Create your models here.
class Standing(models.Model):
    team = Team()
    partidosjugados = models.IntegerField()
    partidosganados = models.IntegerField()
    partidosperdidos = models.IntegerField()
    partidosempatados = models.IntegerField()
    golesafavor = models.IntegerField()
    golesencontra = models.IntegerField()
    golesdiferencia = models.IntegerField()
    puntos = models.IntegerField()
    active = models.BooleanField(default='True')
