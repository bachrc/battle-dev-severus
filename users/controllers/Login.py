import jwt
from django.contrib.auth import user_logged_in
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from battledevseverus import settings
from users.jwt import jwt_payload_handler
from users.models import Utilisateur


class Login(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']

            user = Utilisateur.objects.get(email=email, password=password)
            if user:
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {'name': "%s %s" % (
                        user.first_name, user.last_name), 'token': token}
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a email and a password'}
            return Response(res)