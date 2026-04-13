---
name: oura-report
description: Generate a comprehensive daily Oura Ring report with all health metrics. Use when the user wants a full daily health summary.
user-invocable: true
---

# Oura Daily Report

Generate a complete daily health report from Oura Ring data.

## Instructions

1. Ask the user which date they want the report for. Default to yesterday if not specified.
2. Run the following commands using the `oura` CLI (activate the venv first with `cd ~/Documents/oura-cli && source .venv/bin/activate`):
   - `oura sleep --start DATE --end DATE`
   - `oura activity --start DATE --end DATE`
   - `oura readiness --start DATE --end DATE`
   - `oura heart-rate --start DATE --end DATE`
   - `oura stress --start DATE --end DATE`
   - `oura resilience --start DATE --end DATE`
   - `oura workouts --start DATE --end DATE`
3. Compile all results into a clean, structured report in English.
4. Add a brief health interpretation at the end:
   - Sleep: evaluate duration (ideal 7-9h), efficiency (>85% good), deep sleep (>1h ideal), REM (>1.5h ideal), HRV (higher is better)
   - Activity: evaluate steps, active calories, high activity time
   - Readiness: score interpretation (85+ excellent, 70-84 good, <70 take it easy)
   - Stress: ratio of stress vs recovery time
   - Heart rate: resting HR trends (lower is generally better for athletes)
5. Keep interpretations concise - 2-3 sentences max per category.
