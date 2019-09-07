from django.db import models

from lobby.models import Question
from users.models import Utilisateur


class Probleme(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=100)
    contenu = models.TextField(max_length=10000)
    questions = models.ManyToManyField(Question, blank=True)
    index = models.IntegerField(null=False, unique=True)
    image = models.ImageField()

    def get_question(self, user_id: int) -> Question:
        questions_ids = [question.id for question in self.questions.all()]

        question_id_for_user = questions_ids[user_id % len(questions_ids)]

        return self.questions.get(id=question_id_for_user)

    def fetch_previous_problem(self):
        if self.index == 1:
            return None

        return Probleme.objects.get(index=self.index - 1)

    def is_problem_unlocked_for_user(self, user: Utilisateur) -> bool:
        from lobby.models import BonneReponse

        if self.index == 1:
            return True

        previous_problem = self.fetch_previous_problem()

        return BonneReponse.objects.filter(probleme=previous_problem, utilisateur=user).exists()

    def validate_for_user(self, user):
        from lobby.models import BonneReponse

        BonneReponse.objects.create(probleme=self, utilisateur=user)

    def store_invalid_answer(self, user, answer):
        from lobby.models import MauvaiseReponse

        MauvaiseReponse.objects.create(probleme=self, utilisateur=user, reponse_donnee=answer)
