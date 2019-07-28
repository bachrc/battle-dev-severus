from django.db import models

from lobby.models import Question


class Probleme(models.Model):
    contenu = models.CharField(max_length=10000)
    questions = models.ManyToManyField(Question, blank=True)


