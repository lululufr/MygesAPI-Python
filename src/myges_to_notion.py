from src.myges import MyGesAPI
from src.notion import NotionAPI
import datetime

import os
import dotenv
import re

import json



def import_myges_to_notion_calendar(database_id, nb_of_day):

        notion = NotionAPI()

        notion.delete_notion_calendar_old_event(database_id)

        print("creation des nouveaux événements")

        myges = MyGesAPI()
        GESevents = myges.get_agenda(nb_of_day)

        cpt = 0
        size = len(GESevents["result"])
        for GESevent in GESevents["result"]:
            cpt += 1
            notion.create_event(database_id, GESevent)
            print(f"Event {cpt}/{size}")