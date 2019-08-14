from django.db import models

from lobby.models import Question


class Probleme(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=100)
    contenu = models.CharField(max_length=10000)
    questions = models.ManyToManyField(Question, blank=True)
    index = models.IntegerField(null=False, unique=True)

    def get_question(self, user_id: int) -> Question:
        questions_ids = [question.id for question in self.questions.all()]

        question_id_for_user = questions_ids[user_id % len(questions_ids)]

        return self.questions.get(id=question_id_for_user)