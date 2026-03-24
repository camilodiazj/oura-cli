---
name: oura-sleep
description: Analyze sleep patterns from Oura Ring data with detailed insights. Use when the user wants to understand their sleep quality.
user-invocable: true
---

# Oura Sleep Analysis

Provide a detailed sleep analysis from Oura Ring data.

## Instructions

1. Determine the date range: default to last 7 days if not specified.
2. Run using the `oura` CLI (activate the venv first with `cd ~/Documents/oura-cli && source .venv/bin/activate`):
   - `oura sleep --start START --end END --json`
3. From the JSON data, analyze:
   - **Duration**: total sleep per night, trend, average
   - **Sleep stages**: deep, light, REM distribution per night. Ideal ratios: Deep 15-20%, REM 20-25%, Light 50-60%
   - **Efficiency**: percentage of time in bed actually sleeping (>90% is excellent)
   - **Heart rate**: average HR during sleep, lowest HR, trend over the period
   - **HRV**: average HRV during sleep, trend (higher = better recovery)
   - **Timing**: bedtime and wake time consistency (from bedtime_start, bedtime_end)
   - **Restlessness**: restless_periods count, latency (time to fall asleep)
4. Present the analysis in Spanish with:
   - A night-by-night breakdown table
   - Sleep architecture analysis (are you getting enough deep/REM?)
   - Recovery indicators (HRV and HR trends)
   - Sleep consistency score (how regular are bed/wake times?)
   - 2-3 specific, actionable recommendations based on the data
5. Flag any concerning patterns:
   - Deep sleep consistently under 45 minutes
   - HRV declining trend
   - High latency (>20 min to fall asleep)
   - Low efficiency (<85%)
   - Irregular sleep schedule (>1h variation in bedtime)
