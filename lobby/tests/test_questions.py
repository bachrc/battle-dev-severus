import logging
import os
import shutil
import tempfile
from datetime import timedelta
from pathlib import Path

from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from lobby.models import Question, Probleme, BonneReponse, MauvaiseReponse, BattleDev
from users.models import Utilisateur
from users.tests.auth_utils import compute_auth_header

MAIL_UTILISATEUR_1 = "p.martinet@live.fr"
PASS_UTILISATEUR_1 = "intraitable"
MAIL_UTILISATEUR_2 = "c.lignac@live.fr"
PASS_UTILISATEUR_2 = "miammanger"

ID_PROBLEME_1 = 1
ID_PROBLEME_2 = 2
ID_PROBLEME_3 = 3

TITRE_PROBLEME_1 = "Roberto le sacré coquin"
CONTENU_PROBLEME_1 = "Roberto est l'homme de ménage de l'archiduchesse"
TITRE_PROBLEME_2 = "Epreuve d'allemand"
CONTENU_PROBLEME_2 = "C'est important de bien connaitre l'allemand, voici vos questions."
TITRE_PROBLEME_3 = "Une blague vraiment marrante"
CONTENU_PROBLEME_3 = "Faites moi confiance, cette blague est vraiment sympa."

INTITULE_QUESTION_1 = "Les chaussettes de l'archiduchesse sont-elles sèches ?"
REPONSE_QUESTION_1 = "Non, Roberto les a encore oublié dans la machine du coup elles ont moisi, sacré Roberto"
INTITULE_QUESTION_2 = "Pourquoi n'a-t-on pas encore viré Roberto ?"
REPONSE_QUESTION_2 = "Car il est là depuis bien trop longtemps et ça couterait trop cher de le virer !"
INTITULE_QUESTION_3 = "Comment dit-on \"Salade de pommes de terre\" en Allemand ?"
REPONSE_QUESTION_3 = "Kartoffelnsalat"
INTITULE_QUESTION_4 = "Comment les abeilles communiquent-elles ?"
REPONSE_QUESTION_4 = "Par e-miel"

logger = logging.getLogger(__name__)
MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ProblemsTest(APITestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self) -> None:
        self.utilisateur1 = Utilisateur.objects.create_user(id=1, last_name="Martinet", first_name="Pierre",
                                                            email=MAIL_UTILISATEUR_1, password=PASS_UTILISATEUR_1)
        self.utilisateur2 = Utilisateur.objects.create_user(id=2, last_name="Lignac", first_name="Cyril",
                                                            email=MAIL_UTILISATEUR_2, password=PASS_UTILISATEUR_2)

    def setupClassicProblems(self):
        BattleDev.objects.create(
            nom="Battle Dev La Combe 2000",
            date_debut=timezone.now() - timedelta(hours=1),
            date_fin=timezone.now() + timedelta(hours=2)
        )
        self.question1 = Question.objects.create(intitule=INTITULE_QUESTION_1, reponse=REPONSE_QUESTION_1)
        self.question2 = Question.objects.create(intitule=INTITULE_QUESTION_2, reponse=REPONSE_QUESTION_2)
        self.question3 = Question.objects.create(intitule=INTITULE_QUESTION_3, reponse=REPONSE_QUESTION_3)
        self.question4 = Question.objects.create(intitule=INTITULE_QUESTION_4, reponse=REPONSE_QUESTION_4)

        current_dir = Path(os.path.dirname(os.path.realpath(__file__)))

        self.imageProbleme1 = SimpleUploadedFile(name='fernando1.png',
                                                 content=open(current_dir / "images" / "fernando1.png", 'rb').read(),
                                                 content_type='image/png')
        self.imageProbleme2 = SimpleUploadedFile(name='fernando2.jpg',
                                                 content=open(current_dir / "images" / "fernando2.jpg", 'rb').read(),
                                                 content_type='image/jpeg')
        self.imageProbleme3 = SimpleUploadedFile(name='fernando3.jpg',
                                                 content=open(current_dir / "images" / "fernando3.jpg", 'rb').read(),
                                                 content_type='image/jpeg')
        self.probleme1 = Probleme.objects.create(id=ID_PROBLEME_1, titre=TITRE_PROBLEME_1, contenu=CONTENU_PROBLEME_1,
                                                 index=1, image=self.imageProbleme1)
        self.probleme1.questions.add(self.question1, self.question2)
        self.probleme2 = Probleme.objects.create(id=ID_PROBLEME_2, titre=TITRE_PROBLEME_2, contenu=CONTENU_PROBLEME_2,
                                                 index=2, image=self.imageProbleme2)
        self.probleme2.questions.add(self.question3)
        self.probleme3 = Probleme.objects.create(id=ID_PROBLEME_3, titre=TITRE_PROBLEME_3, contenu=CONTENU_PROBLEME_3,
                                                 index=3, image=self.imageProbleme3)
        self.probleme3.questions.add(self.question4)

    def setupProblemsWithAGoodAnswer(self):
        self.setupClassicProblems()
        BonneReponse.objects.create(probleme=self.probleme1, utilisateur=self.utilisateur1)

    # test methods

    def test_should_fetch_problems_summaries(self):
        self.setupClassicProblems()
        url = reverse('problems-list')
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        response = self.client.get(url, format='json', **auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response=response, text=TITRE_PROBLEME_1)
        self.assertContains(response=response, text=ID_PROBLEME_1)
        self.assertContains(response=response, text=ID_PROBLEME_2)

        self.assertEqual(response.data[0]["image_url"], self.probleme1.image.url)

    def test_should_not_fetch_infos_on_not_unlocked_problems(self):
        self.setupProblemsWithAGoodAnswer()

        url = reverse('problems-list')
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        response = self.client.get(url, format='json', **auth_headers)

        self.assertTrue(response.data[0]["accessible"])
        self.assertEqual(TITRE_PROBLEME_1, response.data[0]["titre"])
        self.assertEqual(self.probleme1.image.url, response.data[0]["image_url"])

        self.assertTrue(response.data[1]["accessible"])
        self.assertEqual(TITRE_PROBLEME_2, response.data[1]["titre"])
        self.assertEqual(self.probleme2.image.url, response.data[1]["image_url"])

        self.assertFalse(response.data[2]["accessible"])
        self.assertEqual("", response.data[2]["titre"])
        self.assertEqual("", response.data[2]["image_url"])

    def test_should_get_problem_details(self):
        self.setupClassicProblems()
        url = reverse('problem-by-id', kwargs={'problem_id': ID_PROBLEME_1})
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        response = self.client.get(url, format='json', **auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response=response, text=ID_PROBLEME_1)
        self.assertContains(response=response, text=TITRE_PROBLEME_1)
        self.assertContains(response=response, text=CONTENU_PROBLEME_1)

    def test_should_get_different_questions_for_different_users(self):
        self.setupClassicProblems()
        question1: Question = self.probleme1.get_question(self.utilisateur1.id)
        question2: Question = self.probleme1.get_question(self.utilisateur2.id)

        self.assertNotEqual(question1.id, question2.id)

    def test_should_not_access_problems_if_not_authenticated(self):
        url = reverse('problems-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_respect_questions_order(self):
        self.setupClassicProblems()

        url = reverse('problems-list')
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        response = self.client.get(url, format='json', **auth_headers)

        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["id"], ID_PROBLEME_1)
        self.assertEqual(response.data[1]["id"], ID_PROBLEME_2)
        self.assertEqual(response.data[2]["id"], ID_PROBLEME_3)

        self.assertEqual(response.data[0]["index"], 1)
        self.assertEqual(response.data[1]["index"], 2)
        self.assertEqual(response.data[2]["index"], 3)

    def test_should_indicate_accessible_problems_and_those_who_arent(self):
        self.setupClassicProblems()

        url = reverse('problems-list')
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        response = self.client.get(url, format='json', **auth_headers)

        self.assertTrue(response.data[0]["accessible"])
        self.assertFalse(response.data[1]["accessible"])
        self.assertFalse(response.data[2]["accessible"])

    def test_should_take_in_order_when_good_answers_are_given(self):
        self.setupProblemsWithAGoodAnswer()

        url = reverse('problems-list')
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        response = self.client.get(url, format='json', **auth_headers)

        self.assertTrue(response.data[0]["accessible"])
        self.assertTrue(response.data[1]["accessible"])
        self.assertFalse(response.data[2]["accessible"])

    def test_shouldnt_allow_consulting_a_problem_which_isnt_unlocked(self):
        self.setupProblemsWithAGoodAnswer()

        url = reverse('problem-by-id', kwargs={'problem_id': ID_PROBLEME_3})
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        response = self.client.get(url, format='json', **auth_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_allow_good_answer(self):
        self.setupClassicProblems()

        url = reverse('submit-answer', kwargs={'problem_id': ID_PROBLEME_1})
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        good_answer = self.probleme1.get_question(self.utilisateur1.id).reponse

        response = self.client.post(url, format='json', data={
            "reponse": good_answer
        }, **auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["correct"])

    def test_should_allow_good_answer_with_different_case(self):
        self.setupClassicProblems()

        url = reverse('submit-answer', kwargs={'problem_id': ID_PROBLEME_1})
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        good_answer = self.probleme1.get_question(self.utilisateur1.id).reponse

        response = self.client.post(url, format='json', data={
            "reponse": good_answer.upper()
        }, **auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["correct"])

    def test_should_allow_good_answer_even_with_spaces_on_both_sides(self):
        self.setupClassicProblems()

        url = reverse('submit-answer', kwargs={'problem_id': ID_PROBLEME_1})
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        good_answer = self.probleme1.get_question(self.utilisateur1.id).reponse

        response = self.client.post(url, format='json', data={
            "reponse": "   {}  ".format(good_answer.upper())
        }, **auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["correct"])

    def test_should_create_a_good_answer_when_given(self):
        self.setupClassicProblems()

        url = reverse('submit-answer', kwargs={'problem_id': ID_PROBLEME_1})
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        good_answer = self.probleme1.get_question(self.utilisateur1.id).reponse

        response = self.client.post(url, format='json', data={
            "reponse": good_answer
        }, **auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["correct"])
        self.assertEqual(BonneReponse.objects.count(), 1)

        bonne_reponse: BonneReponse = BonneReponse.objects.first()

        self.assertEqual(bonne_reponse.probleme, self.probleme1)
        self.assertEqual(bonne_reponse.utilisateur, self.utilisateur1)

    def test_should_store_when_a_bad_answer_is_given(self):
        self.setupClassicProblems()

        url = reverse('submit-answer', kwargs={'problem_id': ID_PROBLEME_1})
        auth_headers = compute_auth_header(self.client, MAIL_UTILISATEUR_1, PASS_UTILISATEUR_1)
        bad_answer = "la mer noire"

        response = self.client.post(url, format='json', data={
            "reponse": bad_answer
        }, **auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["correct"])
        self.assertEqual(MauvaiseReponse.objects.count(), 1)

        mauvaise_reponse: MauvaiseReponse = MauvaiseReponse.objects.first()

        self.assertEqual(mauvaise_reponse.utilisateur, self.utilisateur1)
        self.assertEqual(mauvaise_reponse.probleme, self.probleme1)
        self.assertEqual(mauvaise_reponse.reponse_donnee, bad_answer)
