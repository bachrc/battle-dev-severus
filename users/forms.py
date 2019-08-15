from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Utilisateur


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Utilisateur
        fields = ('first_name', 'last_name', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Utilisateur
        fields = ('first_name', 'last_name', 'email')
