import requests
import re

URL = "https://ksproelia.pl/zawody"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

response.raise_for_status()

html = response.text

print("========= SEARCHING =========")

patterns = [
    r"\d{1,2}lis",
    r"\d{1,2}gru",
    r"\d{1,2}\s*lis",
    r"\d{1,2}\s*gru",
    r"\d{1,2}\slistopada",
    r"\d{1,2}\sgrudnia",
]

for pattern in patterns:
    matches = re.findall(pattern, html, re.IGNORECASE)
    print(pattern, "=>", len(matches))
    print(matches[:10])

with open("proelia.ics", "w") as f:
    f.write("TEST")

print("DONE")
