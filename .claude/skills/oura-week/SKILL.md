---
name: oura-week
description: Generate a weekly Oura Ring summary with trends and patterns. Use when the user wants to see their week in review.
user-invocable: true
---

# Oura Weekly Summary

Generate a weekly health summary with trends from Oura Ring data.

## Instructions

1. Determine the date range: default to the last 7 days (from 7 days ago to yesterday).
2. Run the following commands using the `oura` CLI (activate the venv first with `cd ~/Documents/oura-cli && source .venv/bin/activate`):
   - `oura sleep --start START --end END --json`
   - `oura activity --start START --end END --json`
   - `oura readiness --start START --end END --json`
   - `oura stress --start START --end END --json`
   - `oura resilience --start START --end END --json`
   - `oura workouts --start START --end END --json`
3. Use the JSON output to calculate:
   - **Sleep**: average total duration, average efficiency, average HRV, average resting HR, best/worst night
   - **Activity**: total steps, average daily steps, total active calories, most active day
   - **Readiness**: average score, trend (improving/declining/stable), best/worst day
   - **Stress**: average daily stress time vs recovery time, ratio trend
   - **Workouts**: total count, types, total calories burned
4. Present the summary in English as a structured weekly review with:
   - A header with the date range
   - Key metrics table with daily values
   - Trends section (is sleep improving? is readiness stable?)
   - Highlights (best workout, best sleep night, highest readiness)
   - One actionable recommendation based on the data patterns
5. Use simple ASCII charts or tables where useful to show daily trends.
