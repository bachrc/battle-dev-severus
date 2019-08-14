from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lobby import serializers
from lobby.dto.problems import ProblemContent as ProblemDTO, ProblemAbridged

from lobby.models import Probleme
from lobby.serializers import ProblemsListSerializer
from users.models import Utilisateur


class ProblemsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        problems = Probleme.objects.all().order_by('index')

        user: Utilisateur = Utilisateur.objects.get(id=request.user.id)

        return Response([ProblemAbridged(
            id=pb.id,
            titre=pb.titre,
            index=pb.index,
            accessible=pb.check_if_problem_unlocked_for_user(user)
        ).data for pb in problems])


class ProblemsById(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, problem_id: int):
        probleme = Probleme.objects.get(id=problem_id)
        if probleme is None:
            raise Http404

        question = probleme.get_question(user_id=1)

        dto = ProblemDTO(
            id=probleme.id,
            title=probleme.titre,
            contenu=probleme.contenu,
            question=question.intitule
        )

        return Response(dto.data)
