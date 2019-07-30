from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users.controllers.Login import Login as LoginController


urlpatterns = [
    path('login/', LoginController.as_view(), name="login")
]

urlpatterns = format_suffix_patterns(urlpatterns)
