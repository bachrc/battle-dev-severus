from django.contrib import admin
from .models import Probleme  # add this


class ProblemeAdmin(admin.ModelAdmin):
    list_display = ('contenu',)


# Register your models here.
admin.site.register(Probleme, ProblemeAdmin)