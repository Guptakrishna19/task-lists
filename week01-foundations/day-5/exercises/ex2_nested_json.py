import json

# Simulated API response (nested JSON)
raw = {
    "location": {
        "city": "Mumbai",
        "country": "India"
    },
    "weather": {
        "temp_c": 31,
        "condition": "Partly Cloudy",
        "details": {
            "humidity": 78,
            "wind_kph": 12,
            "uv_index": 6
        }
    },
    "forecast": [
        {"day": "Mon", "high_c": 33, "low_c": 27},
        {"day": "Tue", "high_c": 31, "low_c": 26},
        {"day": "Wed", "high_c": 29, "low_c": 25}
    ]
}

# 1. Access simple nested value
city = raw["location"]["city"]          # dict → dict
temp = raw["weather"]["temp_c"]         # dict → dict
print(f"City: {city}, Temp: {temp}°C")

# 2. Access deeply nested value
humidity = raw["weather"]["details"]["humidity"]    # 3 levels deep
wind     = raw["weather"]["details"]["wind_kph"]
print(f"Humidity: {humidity}%, Wind: {wind} kph")

# 3. Access a list inside JSON
forecast = raw["forecast"]              # this is a list of dicts
for day in forecast:
    print(f"{day['day']}: High {day['high_c']}°C, Low {day['low_c']}°C")

# 4. Safe access with .get()
# .get() returns None instead of crashing if key doesn't exist
uv    = raw["weather"]["details"].get("uv_index")   # exists → 6
rain  = raw["weather"]["details"].get("rainfall")   # missing → None
print(f"UV Index: {uv}, Rainfall: {rain}")

# 5. Normalize - flatten only what you need
normalized = {
    "city"      : raw["location"]["city"],
    "country"   : raw["location"]["country"],
    "temp_c"    : raw["weather"]["temp_c"],
    "condition" : raw["weather"]["condition"],
    "humidity"  : raw["weather"]["details"]["humidity"],
    "wind_kph"  : raw["weather"]["details"]["wind_kph"],
    "forecast"  : raw["forecast"]
}

# 6. Save normalized data to JSON file
with open("normalized_weather.json", "w") as f:
    json.dump(normalized, f, indent=4)

print("\nNormalized data saved to normalized_weather.json")
print("Normalized dict:", normalized)