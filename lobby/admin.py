from django.contrib import admin

from .models import Probleme, Question


class ProblemeAdmin(admin.ModelAdmin):
    list_display = ('contenu',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('intitule',)


# Register your models here.
admin.site.register(Probleme, ProblemeAdmin)
admin.site.register(Question, QuestionAdmin)
