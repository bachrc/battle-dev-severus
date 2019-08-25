from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lobby.dto.battledev import BattleDev as BattleDevDto
from lobby import models


class BattleDev(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Pour le moment, cette méthode ne renvoie que la battle dev courante. La seule et unique dans la base de données.
        A l'avenir, si ce programme sert toujours, nous devons implémenter la restriction des utilisateur à une seule
        battle dev, et n'agir qu'en fonction de la battle dev à laquelle l'utilisateur est lié
        :param request:
        :return:
        """
        battle_dev = models.BattleDev.objects.first()

        return Response(BattleDevDto.from_model(battle_dev).data)
