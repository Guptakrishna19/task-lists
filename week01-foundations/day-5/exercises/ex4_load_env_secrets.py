import os

from dotenv import load_dotenv


# Exercise 4: Load .env secrets
# .env files are used to store secret values like API keys.
# We should not write real API keys directly inside Python code.


# --- 1. Create a sample .env file ---------------------------------------
# In real projects, you usually create this file manually.
with open(".env", "w") as f:
    f.write("WEATHER_API_KEY=demo_weather_key\n")
    f.write("CRYPTO_API_KEY=demo_crypto_key\n")
    f.write("CITY=Mumbai\n")


# --- 2. Load values from .env -------------------------------------------
load_dotenv(".env")

weather_api_key = os.getenv("WEATHER_API_KEY")
crypto_api_key = os.getenv("CRYPTO_API_KEY")
city = os.getenv("CITY")

print("Weather API key:", weather_api_key)
print("Crypto API key:", crypto_api_key)
print("City:", city)


# --- 3. Handle missing secrets safely -----------------------------------
missing_key = os.getenv("MISSING_API_KEY")

if missing_key is None:
    print("MISSING_API_KEY was not found in .env")
else:
    print("Missing API key:", missing_key)


# --- 4. Use the secret in an API URL -------------------------------------
weather_url = f"https://api.example.com/weather?city={city}&key={weather_api_key}"
print("Example API URL:", weather_url)


# OUTPUT
"""
Weather API key: demo_weather_key
Crypto API key: demo_crypto_key
City: Mumbai
MISSING_API_KEY was not found in .env
Example API URL: https://api.example.com/weather?city=Mumbai&key=demo_weather_key
"""
