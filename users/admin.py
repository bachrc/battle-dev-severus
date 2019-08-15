from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Utilisateur


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    ordering = ('email',)
    model = Utilisateur
    list_display = ['email', 'first_name', 'last_name']

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Infos perso', {
            'fields': ('first_name', 'last_name',)
        }),
        ('Privileges', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


admin.site.register(Utilisateur, CustomUserAdmin)
