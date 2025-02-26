from datetime import datetime, timedelta
import base64
import os
import re
import requests
from dotenv import load_dotenv


AUTH_URL = "https://authentication.kordis.fr/oauth/authorize?response_type=token&client_id=skolae-app"


class MyGesAPI:
    """Client API pour  MyGes"""

    BASE_URL = "https://api.kordis.fr/me/"

    COMMON_HEADERS = {
        "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (Poulet a la moutarde) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Accept-Language": "fr-FR,fr;q=0.9",
    }

    def __init__(self):
        self.headers = self.COMMON_HEADERS
        self._load_credentials()
        self._authenticate()

    def _authenticate(self):
        auth_headers = self.headers
        auth_headers.update(
            {
                "Authorization": f"Basic {self._get_basic_auth_token()}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )

        response = requests.get(
            self.auth_url, headers=auth_headers, allow_redirects=False
        )

        if response.status_code != 302:
            raise AuthenticationError("Échec de l'authentification")

        self._extract_auth_token(response.headers["location"])

    def _load_credentials(self):
        if not load_dotenv():
            raise ValueError("Erreur fichier .env ")

        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.auth_url = AUTH_URL

        if not all([self.username, self.password, self.auth_url]):
            raise ValueError("Variables manquantes dans le .env")

    def _extract_auth_token(self, location_header):
        try:
            token_match = re.search(r"access_token=([^&]*)", location_header)
            self.headers["Authorization"] = f"Bearer {token_match.group(1)}"
        except:
            print("Impossible d'extraire le token d'authentification")
            exit(1)

    def _get_basic_auth_token(self):
        auth_string = f"{self.username}:{self.password}".encode("ascii")
        return base64.b64encode(auth_string).decode("ascii")

    def _make_request(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params, timeout=10)

        response.raise_for_status()
        return response.json()

    def get_profile(self):
        return self._make_request("profile")

    def get_agenda(self, start_date=None, end_date=None):
        today = datetime.now()

        start = start_date or today.replace(day=1)
        end = end_date or start + timedelta(days=60)

        return self._make_request(
            "agenda",
            params={
                "start": int(start.timestamp()) * 1000,
                "end": int(end.timestamp()) * 1000,
            },
        )
