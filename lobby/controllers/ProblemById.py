from rest_framework.response import Response
from rest_framework.views import APIView

from lobby.models import Probleme
from lobby.serializers import ProblemsListSerializer


class ProblemsById(APIView):

    def get(self, request, problem_id: int):
        return Response("oui : ")