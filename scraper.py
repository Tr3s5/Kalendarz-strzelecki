import requests
import re
import uuid

from datetime import datetime
from icalendar import Calendar, Event

URL = "https://ksproelia.pl/zawody"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

response.raise_for_status()

html = response.text

calendar = Calendar()
calendar.add("prodid", "-//KS Proelia Calendar//")
calendar.add("version", "2.0")

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

print("Found:", matches)

current_year = datetime.now().year
added = set()

for day, month_name in matches:

    key = f"{day}-{month_name}"

    if key in added:
        continue

    added.add(key)

    event_date = datetime(
        current_year,
        months[month_name.lower()],
        int(day),
        10,
        0,
    )

    event = Event()

    event.add(
        "summary",
        f"Zawody KS Proelia - {day} {month_name}"
    )

    event.add("dtstart", event_date)
    event.add("dtend", event_date.replace(hour=16))
    event.add("uid", str(uuid.uuid4()))

    calendar.add_component(event)

with open("proelia.ics", "wb") as f:
    f.write(calendar.to_ical())

print(f"Generated {len(added)} events")
