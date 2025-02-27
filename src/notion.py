import json
import requests
import dotenv
import os
import datetime
import re

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
        try:
            rooms = [{"name": room["name"]} for room in event["rooms"]]
        except (KeyError, TypeError):
            rooms = [{"name": "Aucune salle"}]

        try:
            campus = event["rooms"][0]["campus"]
        except (KeyError, TypeError, IndexError):
            campus = "Campus inconnu"  # Or a suitable default value

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

    def delete_event(self, block_id):
        url = f"{self.BASE_URL}/blocks/{block_id}"
        response = requests.delete(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def delete_notion_calendar_old_event(self, database_id):
        """Efface TOUT les événements plus vieux que aujourd'hui"""
        NotionEvents = self.get_events_database(database_id)

        tz = datetime.timezone(datetime.timedelta(hours=1))

        now = datetime.datetime.now(tz=tz)
        date_aujourdhui = datetime.datetime.combine(
            now.date(), datetime.time(17, 30, 0, tzinfo=tz)
        )
        date_iso = date_aujourdhui.isoformat(timespec="milliseconds")
        print("Suppression des evenements plus vieux que : ", date_iso)

        for event in NotionEvents["results"]:
            try:
                match = re.search(r".*-(.+)$", event["url"])

                notion_start = event["properties"]["Date"]["date"]["start"]
                print("Notion start brute :", notion_start)

                notion_start_dt = datetime.datetime.fromisoformat(notion_start)

                if notion_start_dt > date_aujourdhui:
                    print("Suppression :", notion_start_dt)
                    self.delete_event(match.group(1))
            except:
                print("erreur suppression")
