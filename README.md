# oura-cli

CLI tool to access your Oura Ring data from the terminal. Uses OAuth2 for secure authentication and stores tokens in your system keychain.

Includes [Claude Code](https://claude.ai/claude-code) skills for AI-powered health analysis.

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
git clone https://github.com/camilodiazj/oura-cli.git
cd oura-cli
python3 -m venv .venv
source .venv/bin/activate
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
oura resilience
oura workouts
oura sessions
oura tags
oura ring

# Date range
oura sleep --start 2026-03-01 --end 2026-03-24

# Raw JSON output (useful for scripting)
oura sleep --json

# Specific document by ID
oura sleep --id DOCUMENT_ID

# Help
oura --help
oura sleep --help
```

### Available Commands

| Command | Description |
|---------|-------------|
| `oura me` | Personal info (age, weight, height) |
| `oura sleep` | Sleep duration, stages, efficiency, HR, HRV |
| `oura activity` | Steps, calories, activity time by intensity |
| `oura readiness` | Readiness score and contributors |
| `oura heart-rate` | Heart rate by source (rest, awake, workout) |
| `oura stress` | High stress vs recovery time |
| `oura resilience` | Resilience level and contributors |
| `oura workouts` | Auto-detected and manual workouts |
| `oura sessions` | Guided/unguided sessions |
| `oura tags` | User-entered tags |
| `oura ring` | Ring hardware and configuration |
| `oura spo2` | SpO2 average (requires subscription) |
| `oura vo2max` | VO2 Max estimate (requires subscription) |
| `oura cardio-age` | Cardiovascular age (requires subscription) |

### Common Options

All data commands support:

- `--start, -s` Start date (YYYY-MM-DD), defaults to today
- `--end, -e` End date (YYYY-MM-DD), defaults to today
- `--json` Raw JSON output for scripting/piping
- `--id` Fetch a specific document by ID

## Claude Code Skills

This project includes four AI-powered skills for [Claude Code](https://claude.ai/claude-code) that analyze your Oura data and provide health insights.

### Install Skills

Skills are automatically available when you run Claude Code inside the project directory. To make them available **globally** (in any directory):

```bash
cp -r .claude/skills/oura-report ~/.claude/skills/
cp -r .claude/skills/oura-week ~/.claude/skills/
cp -r .claude/skills/oura-sleep ~/.claude/skills/
cp -r .claude/skills/oura-training ~/.claude/skills/
```

### Available Skills

#### `/oura-report`
Generates a comprehensive daily health report covering sleep, activity, readiness, heart rate, stress, and resilience. Includes health interpretations for each category.

```
> /oura-report
```

#### `/oura-week`
Weekly summary with trends across all metrics. Calculates averages, identifies best/worst days, and shows whether your health indicators are improving or declining.

```
> /oura-week
```

#### `/oura-sleep`
Deep sleep analysis over a period. Evaluates sleep architecture (deep/light/REM ratios), consistency, HRV trends, and flags concerning patterns like low deep sleep or irregular schedules.

```
> /oura-sleep
```

#### `/oura-training`
Training readiness evaluation. Analyzes readiness, sleep quality, HRV trends, recent training load, and stress/recovery ratio to give a clear verdict:

- **ENTRENA FUERTE** - All systems go
- **ENTRENA MODERADO** - Mixed signals, keep intensity in check
- **RECUPERACION ACTIVA** - Light movement only
- **DESCANSA** - Multiple red flags, take the day off

```
> /oura-training
```

## Security

- OAuth2 tokens are stored in your **system keychain** (macOS Keychain, Windows Credential Locker, or Linux Secret Service), not in plain text files
- Client credentials are stored in `~/.config/oura-cli/config.json`
- Tokens auto-refresh when expired
- Run `oura logout` to clear all stored tokens
- Never commit your `.env`, `config.json`, or token files (covered by `.gitignore`)

## License

MIT
