from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

from users.controllers.Login import Login as LoginController
from users.controllers.Whoami import Whoami as WhoamiController

urlpatterns = [
    path('login', LoginController.as_view(), name="login"),
    path('whoami', WhoamiController.as_view(), name="whoami"),
    path('auth-jwt-refresh', refresh_jwt_token),
    path('auth-jwt-verify', verify_jwt_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
