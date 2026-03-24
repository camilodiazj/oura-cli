# oura-cli

CLI tool to access your Oura Ring data from the terminal. Uses OAuth2 for secure authentication and stores tokens in your system keychain.

## Prerequisites

- Python 3.10+
- An Oura Ring with active membership (Gen3/Ring 4)
- An OAuth2 application registered at [developer.ouraring.com](https://developer.ouraring.com/applications)

## Setup

### 1. Register an OAuth2 Application

1. Go to [developer.ouraring.com/applications](https://developer.ouraring.com/applications)
2. Create a new application with:
   - **Redirect URI**: `http://localhost:8932/callback`
   - **Scopes**: Select all that you want to access
3. Note your **Client ID** and **Client Secret**

### 2. Install

```bash
git clone https://github.com/cdiazjaimes/oura-cli.git
cd oura-cli
pip install -e .
```

### 3. Login

```bash
oura login --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
```

This opens your browser for Oura authorization. After approving, tokens are stored securely in your system keychain.

## Usage

```bash
# Personal info
oura me

# Today's data
oura sleep
oura activity
oura readiness
oura heart-rate
oura stress
oura spo2
oura vo2max
oura resilience
oura cardio-age
oura workouts
oura sessions
oura tags
oura ring

# Date range
oura sleep --start 2026-03-01 --end 2026-03-24

# Raw JSON output
oura sleep --json

# Specific document
oura sleep --id DOCUMENT_ID

# Help
oura --help
oura sleep --help
```

## Security

- OAuth2 tokens are stored in your **system keychain** (macOS Keychain, Windows Credential Locker, or Linux Secret Service), not in plain text files
- Client credentials are stored in `~/.config/oura-cli/config.json`
- Tokens auto-refresh when expired
- Run `oura logout` to clear all stored tokens

## License

MIT
