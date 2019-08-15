from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from lobby.controllers.Problems import ProblemsList, ProblemsById, ProblemAnswer

urlpatterns = [
    path('problems/', ProblemsList.as_view(), name="problems-list"),
    path('problems/<int:problem_id>', ProblemsById.as_view(), name="problem-by-id"),
    path('problems/<int:problem_id>/answer', ProblemAnswer.as_view(), name="submit-answer")

]

urlpatterns = format_suffix_patterns(urlpatterns)
