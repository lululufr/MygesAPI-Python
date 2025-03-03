#!/bin/python3
from src.myges_to_notion import *
from src.myges import MyGesAPI
from src.notion import NotionAPI

DATABASE_ID = os.getenv("DATABASE_ID")

# Exemple d'utilisation

myges = MyGesAPI()

notion = NotionAPI()

import_myges_to_notion_calendar(DATABASE_ID, 30)
