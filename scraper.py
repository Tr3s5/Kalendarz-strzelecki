import requests
import re
import uuid
import json

from datetime import datetime
from icalendar import Calendar, Event

calendar = Calendar()
calendar.add("prodid", "-//Kalendarz Strzelecki//")
calendar.add("version", "2.0")

# =========================
# PROELIA
# =========================

URL = "https://ksproelia.pl/zawody"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

response.raise_for_status()

html = response.text

months = {
    "sty": 1,
    "lut": 2,
    "mar": 3,
    "kwi": 4,
    "maj": 5,
    "cze": 6,
    "lip": 7,
    "sie": 8,
    "wrz": 9,
    "paź": 10,
    "lis": 11,
    "gru": 12,
}

pattern = r"(\d{1,2})\s+(sty|lut|mar|kwi|maj|cze|lip|sie|wrz|paź|lis|gru)"

matches = re.findall(pattern, html, re.IGNORECASE)

current_year = datetime.now().year
added = set()

for day, month_name in matches:

    key = f"{day}-{month_name}"

    if key in added:
        continue

    added.add(key)

    dt_start = datetime(
        current_year,
        months[month_name.lower()],
        int(day),
        10,
        0
    )

    event = Event()

    event.add(
        "summary",
        f"KS Proelia - {day} {month_name}"
    )

    event.add("dtstart", dt_start)
    event.add("dtend", dt_start.replace(hour=16))
    event.add("uid", str(uuid.uuid4()))

    calendar.add_component(event)

# =========================
# CUSTOM EVENTS
# =========================

try:

    with open("custom_events.json", "r", encoding="utf-8") as f:
        custom_events = json.load(f)

    for item in custom_events:

        start_dt = datetime.strptime(
            f"{item['date']} {item['start']}",
            "%Y-%m-%d %H:%M"
        )

        end_dt = datetime.strptime(
            f"{item['date']} {item['end']}",
            "%Y-%m-%d %H:%M"
        )

        event = Event()

        event.add("summary", item["title"])
        event.add("location", item.get("location", ""))

        event.add("dtstart", start_dt)
        event.add("dtend", end_dt)

        event.add("uid", str(uuid.uuid4()))

        calendar.add_component(event)

except FileNotFoundError:
    print("custom_events.json not found")

# =========================
# SAVE ICS
# =========================

with open("proelia.ics", "wb") as f:
    f.write(calendar.to_ical())

print(f"Generated {len(added)} Proelia events")
