from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lobby.dto.problems import ProblemContent as ProblemDTO, ProblemAbridged, AnswerResult
from lobby.models import Probleme
from lobby.permissions import BattleDevHasBegan, CanAccessProblem
from users.models import Utilisateur


class ProblemsList(APIView):
    permission_classes = (IsAuthenticated, BattleDevHasBegan)

    def get(self, request):
        problems = Probleme.objects.all().order_by('index')

        return Response([self._render_problem(pb, request.user) for pb in problems])

    def _render_problem(self, pb: Probleme, user: Utilisateur):
        if pb.is_problem_unlocked_for_user(user):
            return self._render_unlocked_problem(pb).data

        return self._render_locked_problem(pb).data

    def _render_locked_problem(self, pb: Probleme):
        return ProblemAbridged(
            id=pb.id,
            titre="",
            index=pb.index,
            accessible=False,
            image_url=""
        )

    def _render_unlocked_problem(self, pb: Probleme):
        return ProblemAbridged(
            id=pb.id,
            titre=pb.titre,
            index=pb.index,
            accessible=True,
            image_url=pb.image.url
        )


class ProblemsById(APIView):
    permission_classes = (IsAuthenticated, BattleDevHasBegan, CanAccessProblem)

    def get(self, request, problem_id: int):
        user = request.user
        problem = get_problem_if_available(problem_id)

        question = problem.get_question(user.id)

        dto = ProblemDTO(
            id=problem.id,
            title=problem.titre,
            contenu=problem.contenu,
            question=question.intitule
        )

        return Response(dto.data)


class ProblemAnswer(APIView):
    permission_classes = (IsAuthenticated, BattleDevHasBegan, CanAccessProblem)

    def post(self, request, problem_id: int):
        user = request.user
        problem = get_problem_if_available(problem_id)
        question = problem.get_question(user.id)
        answer = request.data["reponse"]

        if not question.is_correct_answer(answer):
            problem.store_invalid_answer(user, answer)
            return Response(AnswerResult(correct=False, details="Réponse incorrecte.").data)

        problem.validate_for_user(user)

        return Response(AnswerResult(correct=True, details="Bonne réponse, bravo !").data)


def get_problem_if_available(problem_id) -> Probleme:
    problem = Probleme.objects.get(id=problem_id)
    if problem is None:
        raise Http404

    return problem
