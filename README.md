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
python manage.py runserver 0.0.0.0:8000
``` 

Le serveur fonctionne, prêt à partir !

## Variables d'environnement

Voici une liste des variables d'environnement que vous pouvez surcharger.

|Intitulé de variable    | Valeur                                                            |
|------------------------|-------------------------------------------------------------------|
|`SEVERUS_SECRET_KEY`    | Token privé servant notamment à la signature du jeton JWT         |
|`SEVERUS_DEBUG`         | Activer le mode debug pour l'application. Peut-être `0` ou `1`    |
|`SEVERUS_APP_DB_ENGINE` | Driver de base de données. Défaut sur `django.db.backends.sqlite3`|
|`SEVERUS_DB_NAME`       | Nom de la base de données.                                        |
|`SEVERUS_DB_HOST`       | Hôte de la base de données.                                       |
|`SEVERUS_DB_PORT`       | Port de la base de données.                                       |
|`SEVERUS_DB_USER`       | Utilisateur ayant les droits sur la base de données.              |
|`SEVERUS_DB_PASSWORD`   | Le mot de passe de l'utilisateur.                                 |
