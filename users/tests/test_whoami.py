from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Utilisateur
from users.tests.auth_utils import compute_auth_header

ID_UTILISATEUR_1 = 1
PRENOM_UTILISATEUR_1 = "Pierre"
NOM_UTILISATEUR_1 = "Martinet"
MAIL_UTILISATEUR_1 = "p.martinet@live.fr"
PASS_UTILISATEUR_1 = "intraitable"


class WhoamiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.utilisateur1 = Utilisateur.objects.create_user(id=ID_UTILISATEUR_1,
                                                           last_name=NOM_UTILISATEUR_1,
                                                           first_name=PRENOM_UTILISATEUR_1,
                                                           email=MAIL_UTILISATEUR_1,
                                                           password=PASS_UTILISATEUR_1)

    def test_should_return_correct_info_for_whoami(self):
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)

        url_whoami = reverse("whoami")
        response_whoami = self.client.get(url_whoami, **auth_headers)
        print(response_whoami)
        self.assertEqual(response_whoami.status_code, status.HTTP_200_OK)
        self.assertEqual(response_whoami.data["id_utilisateur"], ID_UTILISATEUR_1)
        self.assertEqual(response_whoami.data["prenom"], PRENOM_UTILISATEUR_1)
        self.assertEqual(response_whoami.data["nom"], NOM_UTILISATEUR_1)
