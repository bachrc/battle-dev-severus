import jwt
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from battledevseverus import settings
from users.models import Utilisateur


class LoginTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.utilisateur1 = Utilisateur.objects.create_user(id=1, last_name="Martinet", first_name="Pierre",
                                                           email="p.martinet@live.fr", password="intraitable")

    def test_should_authenticate_if_user_exists(self):
        url = reverse('login')
        response = self.client.post(url, {
            "email": "p.martinet@live.fr",
            "password": "intraitable"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)
        self.assertTrue(jwt.decode(response.data["token"], settings.SECRET_KEY))

    def test_should_raise_exception(self):
        url = reverse('login')
        response = self.client.post(url, {
            "email": "p.martinet@live.fr",
            "password": "mauvaismdp"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
