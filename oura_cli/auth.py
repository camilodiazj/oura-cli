"""OAuth2 authentication for Oura API."""

import json
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, urlparse, parse_qs

import keyring
import requests

from .config import load_config, save_config, get_client_credentials

SERVICE_NAME = "oura-cli"
CALLBACK_PORT = 8932


def _store_token(token_data: dict) -> None:
    """Store OAuth2 token data in system keychain."""
    token_data["expires_at"] = time.time() + token_data.get("expires_in", 3600)
    keyring.set_password(SERVICE_NAME, "token_data", json.dumps(token_data))


def _load_token() -> dict | None:
    """Load OAuth2 token data from system keychain."""
    raw = keyring.get_password(SERVICE_NAME, "token_data")
    if raw:
        return json.loads(raw)
    return None


def _clear_token() -> None:
    """Remove OAuth2 token data from system keychain."""
    try:
        keyring.delete_password(SERVICE_NAME, "token_data")
    except keyring.errors.PasswordDeleteError:
        pass


def _refresh_access_token(token_data: dict) -> dict:
    """Refresh the access token using the refresh token."""
    config = load_config()
    client_id, client_secret = get_client_credentials(config)
    refresh_token = token_data.get("refresh_token")
    if not refresh_token:
        raise SystemExit("No refresh token available. Run: oura login")

    resp = requests.post(
        config["token_url"],
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )
    if resp.status_code != 200:
        _clear_token()
        raise SystemExit(f"Token refresh failed ({resp.status_code}). Run: oura login")

    new_token = resp.json()
    if "refresh_token" not in new_token:
        new_token["refresh_token"] = refresh_token
    _store_token(new_token)
    return new_token


def get_access_token() -> str:
    """Get a valid access token, refreshing if needed."""
    token_data = _load_token()
    if not token_data:
        raise SystemExit("Not logged in. Run: oura login")

    if time.time() >= token_data.get("expires_at", 0) - 60:
        token_data = _refresh_access_token(token_data)

    return token_data["access_token"]


def do_login(client_id: str, client_secret: str) -> None:
    """Run the full OAuth2 authorization code flow."""
    config = load_config()
    config["client_id"] = client_id
    config["client_secret"] = client_secret
    save_config(config)

    auth_code = None
    error_msg = None

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal auth_code, error_msg
            params = parse_qs(urlparse(self.path).query)

            if "error" in params:
                error_msg = params["error"][0]
                self._respond("Authorization failed. You can close this tab.")
            elif "code" in params:
                auth_code = params["code"][0]
                self._respond("Login successful! You can close this tab.")
            else:
                self._respond("Unexpected response. You can close this tab.")

        def _respond(self, message: str):
            html = f"<html><body><h2>{message}</h2></body></html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        def log_message(self, format, *args):
            pass  # Suppress HTTP logs

    auth_params = urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": config["redirect_uri"],
        "scope": config["scopes"],
        "state": str(int(time.time())),
    })
    auth_url = f"{config['auth_url']}?{auth_params}"

    server = HTTPServer(("127.0.0.1", CALLBACK_PORT), CallbackHandler)
    print(f"Opening browser for Oura authorization...")
    webbrowser.open(auth_url)
    print(f"Waiting for callback on port {CALLBACK_PORT}...")

    server.handle_request()
    server.server_close()

    if error_msg:
        raise SystemExit(f"Authorization failed: {error_msg}")
    if not auth_code:
        raise SystemExit("No authorization code received.")

    # Exchange code for tokens
    resp = requests.post(
        config["token_url"],
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": config["redirect_uri"],
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )
    if resp.status_code != 200:
        raise SystemExit(f"Token exchange failed ({resp.status_code}): {resp.text}")

    _store_token(resp.json())
    print("Logged in successfully. Tokens stored in system keychain.")


def do_logout() -> None:
    """Clear stored tokens."""
    _clear_token()
    print("Logged out. Tokens removed from keychain.")
