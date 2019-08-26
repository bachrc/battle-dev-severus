from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lobby.dto.problems import ProblemContent as ProblemDTO, ProblemAbridged, AnswerResult
from lobby.models import Probleme
from lobby.permissions import BattleDevHasBegan, CanAccessProblem


class ProblemsList(APIView):
    permission_classes = (IsAuthenticated, BattleDevHasBegan)

    def get(self, request):
        problems = Probleme.objects.all().order_by('index')

        return Response([ProblemAbridged(
            id=pb.id,
            titre=pb.titre,
            index=pb.index,
            accessible=pb.is_problem_unlocked_for_user(request.user)
        ).data for pb in problems])


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
