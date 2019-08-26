from rest_framework.permissions import BasePermission

from lobby import models


class BattleDevHasBegan(BasePermission):
    def has_permission(self, request, view):
        battle_dev = models.BattleDev.objects.first()

        return battle_dev.has_began
