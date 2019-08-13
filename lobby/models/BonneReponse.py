from django.db import models

from lobby.models import Question, Probleme
from users.models import Utilisateur


class BonneReponse(models.Model):
    id = models.AutoField(primary_key=True)
    probleme = models.OneToOneField(Probleme, on_delete=models.CASCADE)
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    date_soumission = models.DateTimeField(auto_now=True)