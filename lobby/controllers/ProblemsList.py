from rest_framework.response import Response
from rest_framework.views import APIView


class ProblemsList(APIView):

    def get(self, request):
        return Response("oui")