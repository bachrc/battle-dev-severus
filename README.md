# Battle dev Severus

Ceci est le dépôt du coordinateur de la Battle Dev de la Combe du Lion Vert.

## Introduction

Severus a été développé dans le but de coordonner toute la Battle Dev.
Il a été réalisé en Python 3.7 avec le framework web Django, le tout en TDD.

Ici, Django ne se charge que des traitements serveur, du "back-end", où il expose
une interface REST ouverte à quiconque voudrait intéragir avec lui. Le contrat
d'interface est notamment disponible dans [le fichier swagger.yml](swagger.yml)

## Déploiement

Par défaut, Django crée une base de données SQLite, mais pour la production, 
veuillez déployer une instance Posrtgresql, en la configurant dans les paramètres
de l'application, idéalement en les surchargeant via les variables d'environnement.

Il vous faut d'abord bien évidemment Python 3.7, et ensuite :

```
pip install -r requirements.txt
python manage.py startapp
``` 

Le serveur fonctionne, prêt à partir !