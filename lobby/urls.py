from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from lobby.controllers.Problems import ProblemsList, ProblemsById

urlpatterns = [
    path('problems/', ProblemsList.as_view(), name="problems-list"),
    path('problems/<int:problem_id>', ProblemsById.as_view(), name="problem-by-id")
]

urlpatterns = format_suffix_patterns(urlpatterns)
