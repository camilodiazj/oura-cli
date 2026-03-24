"""Oura Ring CLI - Access your Oura Ring data from the terminal."""

import json
import functools
from datetime import date, timedelta

import click

from . import __version__
from .auth import do_login, do_logout
from .client import OuraClient
from . import formatters


# -- Shared options decorator --------------------------------------------------

def data_options(f):
    """Add common --start, --end, --json, --id options to a data command."""
    @click.option("--start", "-s", default=None, help="Start date (YYYY-MM-DD). Default: today.")
    @click.option("--end", "-e", default=None, help="End date (YYYY-MM-DD). Default: today.")
    @click.option("--json", "as_json", is_flag=True, help="Output raw JSON.")
    @click.option("--id", "doc_id", default=None, help="Fetch a specific document by ID.")
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper


def _default_dates(start: str | None, end: str | None) -> tuple[str, str]:
    """Return (start, end) dates. End date is shifted +1 day because Oura's API uses exclusive end dates."""
    today = date.today()
    s = start or today.isoformat()
    e = end or today.isoformat()
    # Oura API end_date is exclusive, so add 1 day to include the requested end date
    end_date = date.fromisoformat(e) + timedelta(days=1)
    return s, end_date.isoformat()


# -- Data command factory ------------------------------------------------------

COMMANDS = {
    "sleep": {
        "endpoint": "/v2/usercollection/daily_sleep",
        "formatter": "format_sleep",
        "help": "Daily sleep summary.",
    },
    "activity": {
        "endpoint": "/v2/usercollection/daily_activity",
        "formatter": "format_activity",
        "help": "Daily activity summary.",
    },
    "readiness": {
        "endpoint": "/v2/usercollection/daily_readiness",
        "formatter": "format_readiness",
        "help": "Daily readiness score.",
    },
    "heart-rate": {
        "endpoint": "/v2/usercollection/heartrate",
        "formatter": "format_heart_rate",
        "help": "Heart rate data.",
        "date_params": ("start_datetime", "end_datetime"),
    },
    "stress": {
        "endpoint": "/v2/usercollection/daily_stress",
        "formatter": "format_stress",
        "help": "Daily stress data.",
    },
    "spo2": {
        "endpoint": "/v2/usercollection/daily_spo2",
        "formatter": "format_spo2",
        "help": "Daily SpO2 average.",
    },
    "vo2max": {
        "endpoint": "/v2/usercollection/vO2_max",
        "formatter": "format_vo2max",
        "help": "VO2 Max estimates.",
    },
    "resilience": {
        "endpoint": "/v2/usercollection/daily_resilience",
        "formatter": "format_resilience",
        "help": "Daily resilience score.",
    },
    "cardio-age": {
        "endpoint": "/v2/usercollection/daily_cardiovascular_age",
        "formatter": "format_cardio_age",
        "help": "Cardiovascular age estimate.",
    },
    "workouts": {
        "endpoint": "/v2/usercollection/workout",
        "formatter": "format_workouts",
        "help": "Workout sessions.",
    },
    "sessions": {
        "endpoint": "/v2/usercollection/session",
        "formatter": "format_sessions",
        "help": "Guided and unguided sessions.",
    },
    "tags": {
        "endpoint": "/v2/usercollection/tag",
        "formatter": "format_tags",
        "help": "User-entered tags.",
    },
    "ring": {
        "endpoint": "/v2/usercollection/ring_configuration",
        "formatter": "format_ring_config",
        "help": "Ring configuration and hardware info.",
    },
}


def _make_data_command(name: str, spec: dict):
    """Create a Click command for a data endpoint."""
    endpoint = spec["endpoint"]
    fmt_name = spec["formatter"]
    date_keys = spec.get("date_params", ("start_date", "end_date"))

    @click.command(help=spec["help"])
    @data_options
    @click.pass_context
    def cmd(ctx, start, end, as_json, doc_id):
        client = OuraClient()

        if doc_id:
            data = client.get(f"{endpoint}/{doc_id}")
            if as_json:
                click.echo(json.dumps(data, indent=2))
            else:
                fmt_fn = getattr(formatters, fmt_name)
                click.echo(fmt_fn([data]))
            return

        s, e = _default_dates(start, end)
        params = {date_keys[0]: s, date_keys[1]: e}
        data = client.get_all(endpoint, params)

        if as_json:
            click.echo(json.dumps(data, indent=2))
        else:
            fmt_fn = getattr(formatters, fmt_name)
            click.echo(fmt_fn(data))

    cmd.__doc__ = spec["help"]
    return cmd


# -- CLI group -----------------------------------------------------------------

@click.group()
@click.version_option(__version__, prog_name="oura")
def cli():
    """Oura Ring CLI - Access your Oura Ring data from the terminal."""
    pass


# -- Auth commands -------------------------------------------------------------

@cli.command()
@click.option("--client-id", prompt="Client ID", help="OAuth2 Client ID from developer.ouraring.com")
@click.option("--client-secret", prompt="Client Secret", hide_input=True, help="OAuth2 Client Secret")
def login(client_id, client_secret):
    """Authenticate with your Oura account via OAuth2."""
    do_login(client_id, client_secret)


@cli.command()
def logout():
    """Remove stored authentication tokens."""
    do_logout()


# -- Personal info command -----------------------------------------------------

@cli.command()
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON.")
def me(as_json):
    """Show your personal info."""
    client = OuraClient()
    data = client.get("/v2/usercollection/personal_info")
    if as_json:
        click.echo(json.dumps(data, indent=2))
    else:
        click.echo(formatters.format_personal_info(data))


# -- Register all data commands ------------------------------------------------

for cmd_name, cmd_spec in COMMANDS.items():
    cli.add_command(_make_data_command(cmd_name, cmd_spec), cmd_name)
