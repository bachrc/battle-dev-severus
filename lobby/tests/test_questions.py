import logging

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lobby.models import Question, Probleme

ID_PROBLEME_1 = 1
ID_PROBLEME_2 = 2

TITRE_PROBLEME_1 = "Roberto le sacré coquin"
CONTENU_PROBLEME_1 = "Roberto est l'homme de ménage de l'archiduchesse"
TITRE_PROBLEME_2 = "Epreuve d'allemand"
CONTENU_PROBLEME_2 = "C'est important de bien connaitre l'allemand, voici vos questions."

INTITULE_QUESTION_1 = "Les chaussettes de l'archiduchesse sont-elles sèches ?"
REPONSE_QUESTION_1 = "Non, Roberto les a encore oublié dans la machine du coup elles ont moisi, sacré Roberto"
INTITULE_QUESTION_2 = "Pourquoi n'a-t-on pas encore viré Roberto ?"
REPONSE_QUESTION_2 = "Car il est là depuis bien trop longtemps et ça couterait trop cher de le virer !"
INTITULE_QUESTION_3 = "Comment dit-on \"Salade de pommes de terre\" en Allemand ?"
REPONSE_QUESTION_3 = "Kartoffelnsalat"

logger = logging.getLogger(__name__)


class ProblemsTest(APITestCase):
    def setUp(self):
        self.utilisateur1 = User.objects.create(id=1, last_name="Martinet", first_name="Pierre", email="y.bacha@live.fr", username="pmartinet")
        self.utilisateur2 = User.objects.create(id=2, last_name="Lignac", first_name="Cyril", email="c.lignac@live.fr", username="clignac")
        self.question1 = Question.objects.create(intitule=INTITULE_QUESTION_1, reponse=REPONSE_QUESTION_1)
        self.question2 = Question.objects.create(intitule=INTITULE_QUESTION_2, reponse=REPONSE_QUESTION_2)
        self.question3 = Question.objects.create(intitule=INTITULE_QUESTION_3, reponse=REPONSE_QUESTION_3)

        self.probleme1 = Probleme.objects.create(id=ID_PROBLEME_1, titre=TITRE_PROBLEME_1, contenu=CONTENU_PROBLEME_1)
        self.probleme1.questions.add(self.question1, self.question2)
        self.probleme2 = Probleme.objects.create(id=ID_PROBLEME_2, titre=TITRE_PROBLEME_2, contenu=CONTENU_PROBLEME_2)
        self.probleme2.questions.add(self.question3)

    def test_should_fetch_problems_summaries(self):
        url = reverse('problems-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response=response, text=TITRE_PROBLEME_1)
        self.assertContains(response=response, text=TITRE_PROBLEME_2)
        self.assertContains(response=response, text=ID_PROBLEME_1)
        self.assertContains(response=response, text=ID_PROBLEME_2)

    def test_should_get_problem_details(self):
        url = reverse('problem-by-id', kwargs={'problem_id': ID_PROBLEME_1})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response=response, text=ID_PROBLEME_1)
        self.assertContains(response=response, text=TITRE_PROBLEME_1)
        self.assertContains(response=response, text=CONTENU_PROBLEME_1)

    def test_should_get_different_questions_for_different_users(self):
        question1: Question = self.probleme1.get_question(self.utilisateur1.id)
        question2: Question = self.probleme1.get_question(self.utilisateur2.id)

        self.assertNotEqual(question1.id, question2.id)