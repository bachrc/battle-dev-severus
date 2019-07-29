from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from lobby import serializers
from lobby.dto.Problem import Problem as ProblemDTO
from lobby.models import Probleme


class ProblemsById(APIView):

    def get(self, request, problem_id: int):
        probleme = Probleme.objects.get(id=problem_id)
        if probleme is None:
            raise Http404

        question = probleme.get_question()

        dto = ProblemDTO(
            id_problem=probleme.id,
            title=probleme.titre,
            contenu=probleme.contenu,
            question=question.intitule
        )

        serializer = serializers.ProblemSerializer(dto)

        return Response(serializer.data)
