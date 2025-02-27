from datetime import datetime, timedelta
import base64
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

AUTH_URL = "https://authentication.kordis.fr/oauth/authorize?response_type=token&client_id=skolae-app"
BASE_URL = "https://api.kordis.fr/me/"


class MyGesAPI:
    """Client API pour MyGes"""

    COMMON_HEADERS = {
        "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (Poulet a la moutarde) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Accept-Language": "fr-FR,fr;q=0.9",
    }

    def __init__(self):
        self.headers = self.COMMON_HEADERS.copy()
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.auth_url = AUTH_URL
        self._authenticate()

    def _authenticate(self):
        auth_headers = self.headers.copy()
        auth_headers.update(
            {
                "Authorization": f"Basic {self._get_basic_auth_token()}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )

        response = requests.get(
            self.auth_url, headers=auth_headers, allow_redirects=False
        )
        self._extract_auth_token(response.headers["location"])

    def _extract_auth_token(self, location_header):
        token_match = re.search(r"access_token=([^&]*)", location_header)
        if token_match:
            self.headers["Authorization"] = f"Bearer {token_match.group(1)}"
        else:
            print("Impossible d'extraire le token d'authentification")
            exit(1)

    def _get_basic_auth_token(self):
        auth_string = f"{self.username}:{self.password}".encode("ascii")
        return base64.b64encode(auth_string).decode("ascii")

    def _make_request(self, endpoint, params=None):
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def _post_request(self, endpoint, data):
        url = f"{BASE_URL}{endpoint}"
        response = requests.post(url, headers=self.headers, data=data, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_profile(self):
        return self._make_request("profile")

    def get_agenda(self, number_of_day):
        today = datetime.now()
        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=number_of_day)
        return self._make_request(
            "agenda",
            params={
                "start": int(start.timestamp()) * 1000,
                "end": int(end.timestamp()) * 1000,
            },
        )

    def get_grades(self, years):
        return self._make_request(f"{years}/grades")

    def get_absences(self, years):
        return self._make_request(f"{years}/absences")

    def get_classes(self, years):
        return self._make_request(f"{years}/classes")

    def get_students(self):
        class_id = self.get_classes(2024)["result"][0]["puid"]
        return self._make_request(f"classes/{class_id}/students")

    def get_student(self, student_id):
        return self._make_request(f"students/{student_id}")

    def get_next_events(self):
        today = datetime.now()
        req = self._make_request("events")
        res = []
        for event in req['result']:
            event_datetime = datetime.fromtimestamp(event['event_date'] / 1000)
            if event_datetime > today:
                res.append(event)
        return res


    def get_event(self, event_id):
        return self._make_request(f"event/{event_id}")
