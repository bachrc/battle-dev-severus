from rest_framework import serializers

from lobby.dto.problems import ProblemContent as ProblemDTO
from lobby.models import Probleme


class ProblemsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probleme
        fields = ['id', 'titre', 'index']
