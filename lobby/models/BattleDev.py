from django.db import models


class BattleDev(models.Model):
    nom = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
