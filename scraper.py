import requests
from icalendar import Calendar, Event
from datetime import datetime
import uuid
import re

URL = "https://ksproelia.pl/zawody"

response = requests.get(
    URL,
    timeout=30,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
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

pattern = r"(\d{1,2})(sty|lut|mar|kwi|maj|cze|lip|sie|wrz|paź|lis|gru)"

matches = re.findall(pattern, html)

current_year = datetime.now().year
events_count = 0

for day, month_name in matches:
    try:
        dt_start = datetime(
            current_year,
            months[month_name],
            int(day),
            10,
            0,
        )

        event = Event()
        event.add("summary", "Zawody KS Proelia")
        event.add("dtstart", dt_start)
        event.add("dtend", dt_start.replace(hour=16))
        event.add("uid", str(uuid.uuid4()))

        calendar.add_component(event)
        events_count += 1

    except Exception as e:
        print(f"ERROR: {e}")

with open("proelia.ics", "wb") as f:
    f.write(calendar.to_ical())

print("========== DEBUG ==========")
print(html[:2000])
print("===========================")
print(f"Generated {events_count} events")
