from django.db import models


class Question(models.Model):
    intitule = models.CharField(max_length=200)
    reponse = models.CharField(max_length=100)
