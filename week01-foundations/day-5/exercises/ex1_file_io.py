import csv
import json

# ── 1. TXT ──────────────────────────────────────────────
# Write
with open("notes.txt", "w") as f:
    f.write("Day 5: Files, APIs & Environments\n")
    f.write("Learning file I/O today.\n")

# Read
with open("notes.txt", "r") as f:
    content = f.read()
print("TXT content:\n", content)


# ── 2. CSV ──────────────────────────────────────────────
# Write
rows = [
    ["coin", "price", "currency"],   # header
    ["bitcoin", 67000, "USD"],
    ["ethereum", 3500, "USD"],
]

with open("crypto.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# Read
with open("crypto.csv", "r") as f:
    reader = csv.DictReader(f)       # reads each row as a dict
    for row in reader:
        print(f"{row['coin']} costs ${row['price']}")


# ── 3. JSON ─────────────────────────────────────────────
# Write
data = {
    "city": "Mumbai",
    "temp_c": 31,
    "humidity": 78
}

with open("weather.json", "w") as f:
    json.dump(data, f, indent=4)     # indent makes it human-readable

# Read
with open("weather.json", "r") as f:
    loaded = json.load(f)
print("JSON loaded:", loaded)
print("Temperature:", loaded["temp_c"], "°C")


#OUTPUT 
"""
TXT content:   
 Day 5: Files, APIs & Environments
Learning file I/O today.

bitcoin costs $67000
ethereum costs $3500
JSON loaded: {'city': 'Mumbai', 'temp_c': 31, 'humidity': 78}
Temperature: 31 °C
"""