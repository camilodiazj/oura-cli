"""HTTP client for the Oura API with auto-refresh and pagination."""

import requests

from .auth import get_access_token
from .config import load_config


class OuraClient:
    """Thin wrapper around the Oura REST API."""

    def __init__(self):
        config = load_config()
        self.base_url = config["api_base"]
        self._session = requests.Session()
        self._set_auth()

    def _set_auth(self):
        token = get_access_token()
        self._session.headers["Authorization"] = f"Bearer {token}"

    def get(self, endpoint: str, params: dict | None = None) -> dict:
        """GET a single endpoint. Retries once on 401 (token refresh)."""
        url = f"{self.base_url}{endpoint}"
        resp = self._session.get(url, params=params, timeout=30)

        if resp.status_code == 401:
            self._set_auth()
            resp = self._session.get(url, params=params, timeout=30)

        if resp.status_code in (401, 403):
            raise SystemExit(
                "Access denied. Your token may lack the required scope, "
                "or your Oura subscription has expired. Try: oura logout && oura login"
            )
        if resp.status_code == 429:
            raise SystemExit("Rate limit exceeded. Wait a few minutes and try again.")
        if resp.status_code != 200:
            raise SystemExit(f"API error {resp.status_code}: {resp.text}")

        return resp.json()

    def get_all(self, endpoint: str, params: dict | None = None) -> list[dict]:
        """GET all pages of a paginated endpoint, returning combined data."""
        params = dict(params or {})
        all_data = []

        while True:
            result = self.get(endpoint, params)

            if "data" in result:
                all_data.extend(result["data"])
                next_token = result.get("next_token")
                if next_token:
                    params["next_token"] = next_token
                else:
                    break
            else:
                # Single document response (e.g., personal_info)
                return [result] if result else []

        return all_data
