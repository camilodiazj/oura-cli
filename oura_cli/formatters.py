"""Human-readable formatters for Oura API data."""


def _seconds_to_hm(seconds: int | None) -> str:
    if seconds is None:
        return "--"
    h, m = divmod(seconds // 60, 60)
    return f"{h}h {m}m" if h else f"{m}m"


def _score_bar(score: int | None, width: int = 20) -> str:
    if score is None:
        return "[--]"
    filled = round(score / 100 * width)
    return f"[{'#' * filled}{'.' * (width - filled)}] {score}"


def _val(value, unit: str = "", fmt: str = "") -> str:
    if value is None:
        return "--"
    if fmt:
        return f"{value:{fmt}}{unit}"
    return f"{value}{unit}"


def format_personal_info(data: dict) -> str:
    lines = ["Profile"]
    lines.append(f"  Email:  {_val(data.get('email'))}")
    lines.append(f"  Age:    {_val(data.get('age'))}")
    lines.append(f"  Height: {_val(data.get('height'), ' cm')}")
    lines.append(f"  Weight: {_val(data.get('weight'), ' kg')}")
    lines.append(f"  Sex:    {_val(data.get('biological_sex'))}")
    return "\n".join(lines)


def format_sleep(records: list[dict]) -> str:
    if not records:
        return "No sleep data found."
    lines = []
    for r in records:
        day = r.get("day", "?")
        sleep_type = r.get("type", "")
        header = f"\n  {day}"
        if sleep_type and sleep_type != "sleep":
            header += f"  ({sleep_type})"
        lines.append(header)
        lines.append(f"    Total:      {_seconds_to_hm(r.get('total_sleep_duration'))}")
        lines.append(f"    Deep:       {_seconds_to_hm(r.get('deep_sleep_duration'))}")
        lines.append(f"    Light:      {_seconds_to_hm(r.get('light_sleep_duration'))}")
        lines.append(f"    REM:        {_seconds_to_hm(r.get('rem_sleep_duration'))}")
        lines.append(f"    Awake:      {_seconds_to_hm(r.get('awake_time'))}")
        lines.append(f"    Efficiency: {_val(r.get('efficiency'), '%')}")
        avg_hr = r.get('average_heart_rate')
        lines.append(f"    Avg HR:     {_val(round(avg_hr, 1) if avg_hr else None, ' bpm')}")
        lines.append(f"    Avg HRV:    {_val(r.get('average_hrv'), ' ms')}")
        lines.append(f"    Lowest HR:  {_val(r.get('lowest_heart_rate'), ' bpm')}")
    return "Sleep" + "".join(lines)


def format_activity(records: list[dict]) -> str:
    if not records:
        return "No activity data found."
    lines = []
    for r in records:
        day = r.get("day", "?")
        score = r.get("score")
        lines.append(f"\n  {day}  {_score_bar(score)}")
        lines.append(f"    Steps:          {_val(r.get('steps'))}")
        lines.append(f"    Calories:       {_val(r.get('active_calories'))} active / {_val(r.get('total_calories'))} total")
        lines.append(f"    Distance:       {_val(r.get('equivalent_walking_distance'), ' m')}")
        lines.append(f"    High activity:  {_seconds_to_hm(r.get('high_activity_time'))}")
        lines.append(f"    Med activity:   {_seconds_to_hm(r.get('medium_activity_time'))}")
        lines.append(f"    Low activity:   {_seconds_to_hm(r.get('low_activity_time'))}")
        lines.append(f"    Sedentary:      {_seconds_to_hm(r.get('sedentary_time'))}")
    return "Activity" + "".join(lines)


def format_readiness(records: list[dict]) -> str:
    if not records:
        return "No readiness data found."
    lines = []
    for r in records:
        day = r.get("day", "?")
        score = r.get("score")
        lines.append(f"\n  {day}  {_score_bar(score)}")
        lines.append(f"    Temp deviation: {_val(r.get('temperature_deviation'), ' C', '.1f')}")
        c = r.get("contributors", {})
        for key in ("activity_balance", "body_temperature", "hrv_balance",
                     "resting_heart_rate", "sleep_balance", "recovery_index"):
            label = key.replace("_", " ").title()
            lines.append(f"    {label}: {_val(c.get(key))}")
    return "Readiness" + "".join(lines)


def format_heart_rate(records: list[dict]) -> str:
    if not records:
        return "No heart rate data found."
    bpms = [r["bpm"] for r in records if r.get("bpm")]
    if not bpms:
        return "No heart rate samples."
    lines = [
        "Heart Rate",
        f"  Samples: {len(bpms)}",
        f"  Min:     {min(bpms)} bpm",
        f"  Max:     {max(bpms)} bpm",
        f"  Avg:     {sum(bpms) // len(bpms)} bpm",
    ]
    # Group by source
    sources: dict[str, list[int]] = {}
    for r in records:
        src = r.get("source", "unknown")
        sources.setdefault(src, []).append(r.get("bpm", 0))
    if len(sources) > 1:
        lines.append("  By source:")
        for src, vals in sorted(sources.items()):
            lines.append(f"    {src}: avg {sum(vals) // len(vals)} bpm ({len(vals)} samples)")
    return "\n".join(lines)


def format_stress(records: list[dict]) -> str:
    if not records:
        return "No stress data found."
    lines = []
    for r in records:
        day = r.get("day", "?")
        lines.append(f"\n  {day}")
        lines.append(f"    High stress:    {_seconds_to_hm(r.get('stress_high'))}")
        lines.append(f"    High recovery:  {_seconds_to_hm(r.get('recovery_high'))}")
    return "Stress" + "".join(lines)


def format_spo2(records: list[dict]) -> str:
    if not records:
        return "No SpO2 data found."
    lines = []
    for r in records:
        day = r.get("day", "?")
        agg = r.get("spo2_percentage") or {}
        lines.append(f"\n  {day}")
        lines.append(f"    Average: {_val(agg.get('average'), '%')}")
    return "SpO2" + "".join(lines)


def format_vo2max(records: list[dict]) -> str:
    if not records:
        return "No VO2 Max data found."
    lines = []
    for r in records:
        day = r.get("day", "?")
        lines.append(f"  {day}: {_val(r.get('vo2_max'), ' ml/kg/min', '.1f')}")
    return "VO2 Max\n" + "\n".join(lines)


def format_resilience(records: list[dict]) -> str:
    if not records:
        return "No resilience data found."
    lines = []
    for r in records:
        day = r.get("day", "?")
        level = r.get("level", "?")
        lines.append(f"\n  {day}  [{level}]")
        c = r.get("contributors", {})
        lines.append(f"    Sleep recovery:   {_val(c.get('sleep_recovery'))}")
        lines.append(f"    Daytime recovery: {_val(c.get('daytime_recovery'))}")
        lines.append(f"    Stress:           {_val(c.get('stress'))}")
    return "Resilience" + "".join(lines)


def format_cardio_age(records: list[dict]) -> str:
    if not records:
        return "No cardiovascular age data found."
    lines = []
    for r in records:
        day = r.get("day", "?")
        lines.append(f"  {day}: {_val(r.get('vascular_age'))} years")
    return "Cardiovascular Age\n" + "\n".join(lines)


def format_workouts(records: list[dict]) -> str:
    if not records:
        return "No workout data found."
    lines = []
    for r in records:
        day = r.get("day", "?")
        activity = r.get("activity", "?")
        intensity = r.get("intensity", "?")
        lines.append(f"\n  {day}  {activity} [{intensity}]")
        cals = r.get('calories')
        lines.append(f"    Calories: {_val(round(cals) if cals else None, ' kcal')}")
        dist = r.get('distance')
        lines.append(f"    Distance: {_val(round(dist) if dist else None, ' m')}")
        label = r.get("label")
        if label:
            lines.append(f"    Label:    {label}")
    return "Workouts" + "".join(lines)


def format_sessions(records: list[dict]) -> str:
    if not records:
        return "No session data found."
    lines = []
    for r in records:
        day = r.get("day", "?")
        mood = r.get("mood", "")
        lines.append(f"\n  {day}  {r.get('type', '?')} {f'[{mood}]' if mood else ''}")
        lines.append(f"    HR avg: {_val(r.get('average_heart_rate'), ' bpm')}")
        lines.append(f"    HRV avg: {_val(r.get('average_hrv'), ' ms')}")
    return "Sessions" + "".join(lines)


def format_tags(records: list[dict]) -> str:
    if not records:
        return "No tag data found."
    lines = []
    for r in records:
        day = r.get("day", "?")
        tags = r.get("tags", r.get("tag_type_code", "?"))
        lines.append(f"  {day}: {tags}")
    return "Tags\n" + "\n".join(lines)


def format_ring_config(records: list[dict]) -> str:
    if not records:
        return "No ring configuration data found."
    lines = []
    for r in records:
        lines.append(f"  Color:      {_val(r.get('color'))}")
        lines.append(f"  Design:     {_val(r.get('design'))}")
        lines.append(f"  Hardware:   {_val(r.get('hardware_type'))}")
        lines.append(f"  Firmware:   {_val(r.get('firmware_version'))}")
        lines.append(f"  Set up at:  {_val(r.get('set_up_at'))}")
    return "Ring Configuration\n" + "\n".join(lines)
