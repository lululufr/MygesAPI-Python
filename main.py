#!/bin/python3
from src.myges_to_notion import *
from src.myges import MyGesAPI
from src.notion import NotionAPI

DATABASE_ID = os.getenv("DATABASE_ID")

#Exemple d'utilisation

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
