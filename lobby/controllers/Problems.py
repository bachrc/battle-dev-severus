from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lobby.dto.problems import ProblemContent as ProblemDTO, ProblemAbridged
from lobby.models import Probleme


class ProblemsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        problems = Probleme.objects.all().order_by('index')

        return Response([ProblemAbridged(
            id=pb.id,
            titre=pb.titre,
            index=pb.index,
            accessible=pb.check_if_problem_unlocked_for_user(request.user)
        ).data for pb in problems])


class ProblemsById(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, problem_id: int):
        probleme = Probleme.objects.get(id=problem_id)
        if probleme is None:
            raise Http404

        if not probleme.check_if_problem_unlocked_for_user(request.user):
            raise PermissionDenied("Vous n'êtes pas autorisé(e) à consulter ce problème.")

        question = probleme.get_question(user_id=1)

        dto = ProblemDTO(
            id=probleme.id,
            title=probleme.titre,
            contenu=probleme.contenu,
            question=question.intitule
        )

        return Response(dto.data)
