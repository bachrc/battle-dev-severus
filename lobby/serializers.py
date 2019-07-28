from rest_framework import serializers

from lobby.models import Probleme


class ProblemsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probleme
        fields = ['id', 'titre']