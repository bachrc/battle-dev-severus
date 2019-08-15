from django.db import models

from lobby.models import Probleme
from users.models import Utilisateur


class MauvaiseReponse(models.Model):
    probleme = models.ForeignKey(Probleme, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    reponse_donnee = models.CharField(max_length=1000)
    date_soumission = models.DateTimeField(auto_now=True)
