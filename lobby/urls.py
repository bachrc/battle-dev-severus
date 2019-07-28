from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from lobby.controllers import ProblemsList

urlpatterns = [
    path('problems/', ProblemsList.ProblemsList.as_view(), name="problems-list")
]

urlpatterns = format_suffix_patterns(urlpatterns)