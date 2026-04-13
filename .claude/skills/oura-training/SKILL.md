---
name: oura-training
description: Analyze training readiness using Oura Ring data to decide if you should train today. Use when the user wants to know if they should work out.
user-invocable: true
---

# Oura Training Readiness

Evaluate whether the user is ready to train based on Oura Ring recovery data.

## Instructions

1. Run the following commands using the `oura` CLI (activate the venv first with `cd ~/Documents/oura-cli && source .venv/bin/activate`). Get today's and the last 3 days of data for context:
   - `oura readiness --start 3_DAYS_AGO --end TODAY --json`
   - `oura sleep --start 3_DAYS_AGO --end TODAY --json`
   - `oura stress --start 3_DAYS_AGO --end TODAY --json`
   - `oura resilience --start 3_DAYS_AGO --end TODAY --json`
   - `oura workouts --start 3_DAYS_AGO --end TODAY --json`
   - `oura activity --start 3_DAYS_AGO --end TODAY --json`
2. Evaluate training readiness based on:
   - **Readiness score**: 85+ = go hard, 70-84 = moderate, <70 = rest or light
   - **Sleep quality**: total duration (>7h?), efficiency (>85%?), HRV trend
   - **HRV**: compare today vs 7-day baseline. Above baseline = recovered. Below = still recovering.
   - **Resting HR**: lower than usual = good recovery, higher = fatigue/stress
   - **Recent training load**: workouts in last 48h, intensity, calories burned
   - **Stress/Recovery ratio**: high recovery = ready, high stress = needs rest
   - **Resilience level**: strong/exceptional = good capacity, limited = needs rest
3. Give a clear verdict:
   - **TRAIN HARD** - All indicators green: high readiness, good sleep, HRV above baseline, no recent high-intensity workouts
   - **TRAIN MODERATE** - Mixed signals: decent readiness but some fatigue indicators
   - **ACTIVE RECOVERY** - Low readiness or poor sleep: suggest light movement only (walking, stretching, yoga)
   - **REST** - Multiple red flags: low readiness, poor sleep, declining HRV, high stress
4. Include:
   - The verdict with a brief explanation (2-3 sentences)
   - Key metrics that informed the decision
   - Suggested workout type/intensity if training is recommended
   - Estimated recovery time if rest is recommended
