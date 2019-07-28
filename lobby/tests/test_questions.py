from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lobby.models import Question, Probleme

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


class ProblemsTest(APITestCase):
    def setUp(self):
        self.question1 = Question.objects.create(intitule=INTITULE_QUESTION_1, reponse=REPONSE_QUESTION_1)
        self.question2 = Question.objects.create(intitule=INTITULE_QUESTION_2, reponse=REPONSE_QUESTION_2)
        self.question3 = Question.objects.create(intitule=INTITULE_QUESTION_3, reponse=REPONSE_QUESTION_3)

        self.probleme1 = Probleme.objects.create(id=1, titre=TITRE_PROBLEME_1, contenu=CONTENU_PROBLEME_1)
        self.probleme1.questions.add(self.question1, self.question2)
        self.probleme2 = Probleme.objects.create(id=2, titre=TITRE_PROBLEME_2, contenu=CONTENU_PROBLEME_2)
        self.probleme2.questions.add(self.question3)

    def test_should_fetch_problems_summaries(self):
        url = reverse('problems-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response=response, text=TITRE_PROBLEME_1)
        self.assertContains(response=response, text=TITRE_PROBLEME_2)
        self.assertContains(response=response, text="1")
        self.assertContains(response=response, text="2")