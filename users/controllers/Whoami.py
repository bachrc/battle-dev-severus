from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users import dto
from users.dto.Whoami import Whoami as WhoamiDTO
from users.models import Utilisateur


class Whoami(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user: Utilisateur = Utilisateur.objects.get(id=request.user.id)

        dto = WhoamiDTO(id_utilisateur=user.id, prenom=user.first_name, nom=user.last_name)

        return Response(dto.data)
