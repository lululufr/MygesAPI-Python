# MyGes to Notion Calendar Integration

## Fonctionnalités

- Utilisation de l'API myges - simple of use.
  - ( comprend l'inscription a des events )
- Synchronisation du calendrier de MyGes vers Notion.

## A venir 

Plugin n8n 

## Prérequis

- Installation des packages Python suivants :
  - `requests`
  - `python-dotenv`

Vous pouvez installer les dépendances avec pip :

```bash
pip install -r requirements.txt
```

Configuration
Le projet utilise des variables d'environnement pour gérer les informations sensibles. Créez un fichier .env à la racine du projet avec le contenu suivant :

``` .env
# Informations pour l'API MyGes
USERNAME=VotreNomUtilisateur_MyGes
PASSWORD=VotreMotDePasse_MyGes

# Informations pour l'API Notion
NOTION_SECRET=VotreSecretNotion
```

Attention : Ne partagez jamais votre fichier .env et pensez à l'ajouter à votre fichier .gitignore. !!

### Exemples d'utilisation

```python
myges = MyGesAPI()

notion = NotionAPI()

"""Récupérer les événements a venir"""
events = myges.get_next_events()
print(events)

"""Afficher son profile"""
profil = myges.get_profile()
print(profil)

"""Afficher ses notes"""
grades = myges.get_grades(2024)
print(grades)


"""Afficher les etudiants de sa classe année en param"""
student = myges.get_students(2024)
print(student)

"""Agenda Myges"""
agenda = myges.get_agenda(30)
print(agenda)

#### Une API Notion est aussi DISPO 

notion = NotionAPI()

"""importe dans la database id les 30 prochain jour du calendier myges
Attention efface les événements plus vieux que maintenant"""
#import_myges_to_notion_calendar(DATABASE_ID,30)
```

Classe NotionAPI
Cette classe gère :

L'interrogation et la gestion des bases de données Notion.
La conversion des données d'événements MyGes au format compatible Notion.
La création de pages/événements dans Notion.

### Exemples d'utilisation

```python

from src.myges import MyGesAPI
from src.notion import NotionAPI

# Identifiant de la base de données Notion où les événements seront importés
DATABASE_ID = "VotreIDDeDatabaseNotion"

# Instanciation de l'API Notion
notion_api = NotionAPI()

# Importer les événements MyGes dans la base Notion pour les 3 prochains jours
notion_api.import_myges_to_notion_calendar(DATABASE_ID, nb_of_day=3)
```

### Pour le calendrier Notion , il faudra

(la creation automatique de la base de données est en cours de développement)

1. Créer une base de données Notion.
2. Créer un connecteur de base de données Notion : <https://www.notion.so/profile/integrations/internal>
3. Connecter a votre page l'intégration
4. Récupérer l'id de la database ( présent dans l'u)rl de la page de la base de données Notion.)
