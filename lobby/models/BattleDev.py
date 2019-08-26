from django.db import models
from django.utils import timezone


class BattleDev(models.Model):
    nom = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()

    @property
    def has_began(self):
        return timezone.now() > self.date_debut
