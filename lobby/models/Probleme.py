from django.db import models
from lobby.models import Question


class Probleme(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=100)
    contenu = models.CharField(max_length=10000)
    questions = models.ManyToManyField(Question, blank=True)
