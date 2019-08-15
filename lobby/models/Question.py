from django.db import models


class Question(models.Model):
    intitule = models.CharField(max_length=200)
    reponse = models.CharField(max_length=100)

    def is_correct_answer(self, proposal: str) -> bool:
        return self.reponse.lower() == proposal.lower().strip()
