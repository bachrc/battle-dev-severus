from rest_framework.permissions import BasePermission

from lobby.models import Probleme, BattleDev


class BattleDevHasBegan(BasePermission):
    def has_permission(self, request, view):
        battle_dev = BattleDev.objects.first()

        return battle_dev.has_began


class CanAccessProblem(BasePermission):
    def has_permission(self, request, view):
        problem_id = view.kwargs['problem_id']

        problem = Probleme.objects.get(id=problem_id)
        return problem is not None and problem.is_problem_unlocked_for_user(request.user)
