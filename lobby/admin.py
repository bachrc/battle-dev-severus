from django.contrib import admin

from lobby.models import BattleDev
from .models import Probleme, Question


class ProblemeAdmin(admin.ModelAdmin):
    list_display = ('titre',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('intitule',)


class BattleDevAdmin(admin.ModelAdmin):
    list_display = ('nom',)


# Register your models here.
admin.site.register(Probleme, ProblemeAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(BattleDev, BattleDevAdmin)
