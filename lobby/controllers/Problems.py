from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lobby import serializers
from lobby.dto.Problem import Problem as ProblemDTO

from lobby.models import Probleme
from lobby.serializers import ProblemsListSerializer


class ProblemsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        problems = Probleme.objects.all()
        serializer = ProblemsListSerializer(problems, many=True)

        return Response(serializer.data)


class ProblemsById(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, problem_id: int):
        probleme = Probleme.objects.get(id=problem_id)
        if probleme is None:
            raise Http404

        question = probleme.get_question(user_id=1)

        dto = ProblemDTO(
            id_problem=probleme.id,
            title=probleme.titre,
            contenu=probleme.contenu,
            question=question.intitule
        )

        return Response(dto.data)
