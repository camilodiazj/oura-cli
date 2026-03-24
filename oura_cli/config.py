"""Configuration management for oura-cli."""

import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "oura-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS = {
    "redirect_uri": "http://localhost:8932/callback",
    "auth_url": "https://cloud.ouraring.com/oauth/authorize",
    "token_url": "https://api.ouraring.com/oauth/token",
    "api_base": "https://api.ouraring.com",
    "scopes": "email personal daily heartrate workout tag session spo2Daily",
}


def load_config() -> dict:
    """Load config from disk, merged with defaults."""
    config = dict(DEFAULTS)
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config.update(json.load(f))
    return config


def save_config(config: dict) -> None:
    """Save config to disk (only non-default values)."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    to_save = {k: v for k, v in config.items() if k not in DEFAULTS or v != DEFAULTS.get(k)}
    with open(CONFIG_FILE, "w") as f:
        json.dump(to_save, f, indent=2)


def get_client_credentials(config: dict) -> tuple[str, str]:
    """Return (client_id, client_secret) or raise."""
    client_id = config.get("client_id")
    client_secret = config.get("client_secret")
    if not client_id or not client_secret:
        raise SystemExit(
            "No OAuth2 credentials found. Run:\n"
            "  oura login --client-id YOUR_ID --client-secret YOUR_SECRET"
        )
    return client_id, client_secret
