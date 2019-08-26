from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from lobby.models import Question, Probleme, BattleDev
from users.models import Utilisateur
from users.tests.auth_utils import compute_auth_header

MAIL_UTILISATEUR_1 = "p.martinet@live.fr"
PASS_UTILISATEUR_1 = "intraitable"
MAIL_UTILISATEUR_2 = "c.lignac@live.fr"
PASS_UTILISATEUR_2 = "miammanger"


class ProblemsTest(APITestCase):

    def setUp(self) -> None:
        self.utilisateur1 = Utilisateur.objects.create_user(id=1, last_name="Martinet", first_name="Pierre",
                                                            email=MAIL_UTILISATEUR_1, password=PASS_UTILISATEUR_1)
        self.utilisateur2 = Utilisateur.objects.create_user(id=2, last_name="Lignac", first_name="Cyril",
                                                            email=MAIL_UTILISATEUR_2, password=PASS_UTILISATEUR_2)

        self.probleme1 = Probleme.objects.create(
            titre="Le problème de Fernando",
            contenu="Fernando a perdu toute sa paie au Kéno alors qu'on est au début du mois.",
            index=1
        )

        self.probleme2 = Probleme.objects.create(
            titre="Dimitri et les maths",
            contenu="Dimitri est en seconde et adorerait travailler à la NASA, mais il est nul en maths.",
            index=2)

        self.probleme3 = Probleme.objects.create(
            titre="Les courses de mamie Yvette",
            contenu="Mamie Yvette adore faire ses courses le samedi apres midi même si elle est à la retraite.",
            index=3
        )

        self.question1 = Question.objects.create(
            intitule="Pourquoi a-t-il fait ça ?",
            reponse="Puisqu'il touche la douce désillusion d'être riche sans rien faire !"
        )
        self.question2 = Question.objects.create(
            intitule="Est-ce que sa femme va le quitter ?",
            reponse="Oui, car il est irresponsable et a deux enfants !"
        )
        self.probleme1.questions.add(self.question1, self.question2)

        self.question3 = Question.objects.create(
            intitule="Est-ce que Dimitri passe tout son argent dans la drogue pour "
                     "fuir la déception qu'il est pour ses parents ?",
            reponse="Oui !")
        self.probleme2.questions.add(self.question3)

        self.question4 = Question.objects.create(
            intitule="Est-ce que Mamie Yvette a battu son record de personnes bloquées derrière elle ?",
            reponse="Eh oui, avec exactement 4 quarantenaires actifs, et deux enfants qui pleurent !")
        self.probleme3.questions.add(self.question4)

    def test_should_retrieve_correct_informations_about_current_battle_dev(self):
        id_battle_dev = 1
        nom_battle_dev = "Michel"
        maintenant = timezone.now()
        date_debut = maintenant + timedelta(days=2)
        date_fin = maintenant + timedelta(days=3)

        BattleDev.objects.create(id=id_battle_dev, nom=nom_battle_dev, date_debut=date_debut, date_fin=date_fin)

        url = reverse('battle-dev')
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        response = self.client.get(url, format='json', **auth_headers)

        self.assertEqual(response.data["id"], id_battle_dev)
        self.assertEqual(response.data["nom"], nom_battle_dev)
        self.assertEqual(response.data["date_debut"], date_debut.isoformat())
        self.assertEqual(response.data["date_fin"], date_fin.isoformat())

    def test_should_not_access_to_questions_before_battle_dev_begginning(self):
        BattleDev.objects.create(
            nom="Battle Dev La Combe 2000",
            date_debut=timezone.now() + timedelta(days=1),
            date_fin=timezone.now() + timedelta(days=2)
        )

        url = reverse('problems-list')
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        response = self.client.get(url, format='json', **auth_headers)

        self.assertEqual(response.status_code, 403)

    def test_should_not_access_a_problem_before_battle_dev_beginning(self):
        BattleDev.objects.create(
            nom="Battle Dev La Combe 2000",
            date_debut=timezone.now() + timedelta(days=1),
            date_fin=timezone.now() + timedelta(days=2)
        )

        url = reverse('problem-by-id', kwargs={'problem_id': self.probleme1.id})
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        response = self.client.get(url, format='json', **auth_headers)

        self.assertEqual(response.status_code, 403)

    def test_should_not_answer_a_problem_before_battle_dev_beginning(self):
        BattleDev.objects.create(
            nom="Battle Dev La Combe 2000",
            date_debut=timezone.now() + timedelta(days=1),
            date_fin=timezone.now() + timedelta(days=2)
        )

        url = reverse('submit-answer', kwargs={'problem_id': self.probleme1.id})
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        good_answer = self.probleme1.get_question(self.utilisateur1.id).reponse

        response = self.client.post(url, format='json', data={
            "reponse": good_answer
        }, **auth_headers)

        self.assertEqual(response.status_code, 403)
