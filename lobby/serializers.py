from rest_framework import serializers

from lobby.dto.Problem import Problem as ProblemDTO
from lobby.models import Probleme


class ProblemsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probleme
        fields = ['id', 'titre']


class ProblemSerializer(serializers.BaseSerializer):
    def to_representation(self, problem: ProblemDTO):
        return {
            "id": problem.id,
            "titre": problem.title,
            "contenu": problem.contenu,
            "question": problem.question
        }