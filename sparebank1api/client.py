from datetime import datetime
from email import header
from genericpath import exists
import io
import json
from time import time
from .config import Config
from .accounts import AccountsAPI
from .transactions import TransactionsAPI
from .transfers import TransfersAPI
from .child_accounts import ChildAccountsAPI
from typing import Dict, Any
import requests
import secrets
from urllib.parse import urlencode, urlparse, parse_qs
from .config import Config


class SpareBank1API:
    BASE_URL = f"https://api.sparebank1.no"
    AUTH_URL = f"{BASE_URL}/oauth/authorize"
    TOKEN_URL = f"{BASE_URL}/oauth/token"
    API_URL = f"{BASE_URL}/personal/banking"

    def __init__(self, config: Config):
        self.config = config
        self.token: Dict[str, Any] = {}
        self._last_state = None
        self.accounts = AccountsAPI(self)
        self.transactions = TransactionsAPI(self)
        self.transfers = TransfersAPI(self)
        self.child_accounts = ChildAccountsAPI(self)

    def get(self, url: str, **kwargs):
        if not self.ensure_token():
            raise
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.token['access_token']}"
        return requests.get(f"{self.API_URL}/{url}", headers=headers, **kwargs)

    def post(self, url: str, **kwargs):
        self.ensure_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.token['access_token']}"
        return requests.post(f"{self.API_URL}/{url}", headers=headers, **kwargs)

    def authenticate(self):
        if exists("token.json"):
            with io.open("token.json", "r", encoding="utf-8") as f:
                self.token = json.load(f)
                print(
                    f"Imported token, valid until {datetime.fromtimestamp(self.token['expires_at'])}"
                )
                self.ensure_token()
                return

        url = self.get_authorization_url()
        print(f"Go to the following URL to authorize: {url}")
        redirect_response = input("Paste the full redirect URL here: ")
        self.fetch_token(redirect_response)

    def set_token(self, token: Dict[str, Any]):
        self.token = {
            "access_token": token.get("access_token"),
            "expires_at": int(token.get("expires_in", 0)) + int(time()),
            "refresh_token": token.get("refresh_token"),
        }
        print(
            f"New token, valid until {datetime.fromtimestamp(self.token['expires_at'])}"
        )
        with io.open("token.json", "w", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    self.token,
                )
            )

    def get_authorization_url(self):
        state = secrets.token_urlsafe(16)
        params = {
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "response_type": "code",
            "state": state,
            "finInst": self.config.fin_inst,
        }
        url = f"{self.AUTH_URL}?{urlencode(params)}"
        self._last_state = state
        return url

    def fetch_token(self, authorization_response: str):
        # Extract code and state from the redirect URL
        parsed = urlparse(authorization_response)
        query = parse_qs(parsed.query)
        code = query.get("code", [None])[0]
        state = query.get("state", [None])[0]
        if not code or not state:
            raise ValueError("Missing code or state in authorization response.")
        if state != self._last_state:
            raise ValueError("State mismatch. Possible CSRF attack.")
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.config.redirect_uri,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
        }
        response = requests.post(self.TOKEN_URL, data=data)
        response.raise_for_status()
        self.set_token(response.json())

    def refresh_token(self, refresh_token):
        data = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
        response = requests.post(
            self.TOKEN_URL,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        self.set_token(response.json())

    def ensure_token(self, minimum_expire_time=60) -> bool:
        """Check if the current token is valid."""
        if (
            not self.token
            or "access_token" not in self.token
            or "expires_at" not in self.token
        ):
            raise Exception("Not authenticated. Please authenticate first.")

        if int(time()) >= self.token["expires_at"] - minimum_expire_time:
            self.refresh_token(self.token.get("refresh_token"))
            if not self.token or "access_token" not in self.token:
                raise Exception("Failed to refresh token. Please re-authenticate.")

        return True
