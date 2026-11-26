import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime
import uuid

URL = "https://ksproelia.pl/zawody"

response = requests.get(URL, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

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
    "gru": 12
}

for text in soup.stripped_strings:
    try:
        if len(text) >= 5 and text[:2].isdigit():
            day = int(text[:2])
            month_txt = text[2:5].lower()

            if month_txt in months:
                event = Event()

                dt = datetime(
                    datetime.now().year,
                    months[month_txt],
                    day,
                    10,
                    0,
                    0
                )

                event.add("summary", "Zawody KS Proelia")
                event.add("dtstart", dt)
                event.add("dtend", dt.replace(hour=16))
                event.add("uid", str(uuid.uuid4()))

                calendar.add_component(event)

    except Exception:
        pass

with open("proelia.ics", "wb") as f:
    f.write(calendar.to_ical())
