from myges import MyGesAPI
import json
import requests
import dotenv
import os
import datetime

dotenv.load_dotenv()


class NotionAPI:
    NOTION_SECRET = os.getenv("NOTION_SECRET")
    BASE_URL = "https://api.notion.com/v1"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.NOTION_SECRET}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def get_database(self, databases_id):
        url = f"{self.BASE_URL}/databases/{databases_id}"
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_events_database(self, databases_id):
        url = f"{self.BASE_URL}/databases/{databases_id}/query"
        response = requests.post(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def parse_myges_to_notion_event(self, database_id, event):
        rooms = [{"name": room["name"]} for room in event["rooms"]]

        campus = event["rooms"][0]["campus"]

        start_timestamp = event["start_date"] / 1000
        end_timestamp = event["end_date"] / 1000

        tz = datetime.timezone(datetime.timedelta(hours=1))
        start_date = datetime.datetime.fromtimestamp(start_timestamp, tz)
        end_date = datetime.datetime.fromtimestamp(end_timestamp, tz)

        template = {
            "parent": {"database_id": database_id},
            "properties": {
                "Name": {"title": [{"text": {"content": event["name"]}}]},
                "Salle": {
                    "multi_select": rooms
                },  # Correction ici, rooms est déjà une liste
                "Campus": {"rich_text": [{"text": {"content": campus}}]},
                "Date": {
                    "date": {
                        "start": start_date.isoformat(timespec="milliseconds"),
                        "end": end_date.isoformat(timespec="milliseconds"),
                    }
                },
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": "Description de l'événement"},
                            }
                        ]
                    },
                }
            ],
        }

        return template

    def create_event(self, database_id, event):
        url = f"{self.BASE_URL}/pages"
        event = self.parse_myges_to_notion_event(database_id, event)

        response = requests.post(url, headers=self.headers, json=event, timeout=10)
        response.raise_for_status()
        return response.json()

    def import_myges_to_notion_calendar(self, database_id, nb_of_day):
        myges = MyGesAPI()
        events = myges.get_agenda(nb_of_day)

        cpt = 0
        size = len(events["result"])
        for event in events["result"]:
            cpt += 1
            self.create_event(database_id, event)
            print(f"Event {cpt}/{size}")
