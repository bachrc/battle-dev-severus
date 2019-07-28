from rest_framework.response import Response
from rest_framework.views import APIView

from lobby.models import Probleme
from lobby.serializers import ProblemsListSerializer


class ProblemsList(APIView):

    def get(self, request):
        problems = Probleme.objects.all()
        serializer = ProblemsListSerializer(problems, many=True)

        return Response(serializer.data)