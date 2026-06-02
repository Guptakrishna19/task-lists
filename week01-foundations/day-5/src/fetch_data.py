import json
import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


# Day 5 Task:
# Fetch live weather and crypto data, normalize it, and save it to JSON.
# Values like city/coin/API key are loaded from .env.


def fetch_json(url, params=None, headers=None, timeout_seconds=10):
    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        print("Timeout error: API request took too long.")

    except requests.exceptions.HTTPError as error:
        print("HTTP error:", error)

    except requests.exceptions.ConnectionError:
        print("Connection error: Check your internet or API URL.")

    except requests.exceptions.RequestException as error:
        print("Request error:", error)

    except ValueError:
        print("JSON error: API response was not valid JSON.")

    return None


def fetch_weather(city, weather_api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric",
    }

    return fetch_json(url, params=params)


def fetch_crypto(coin_id, currency):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": currency,
        "include_24hr_change": "true",
    }

    return fetch_json(url, params=params)


def normalize_weather(raw_weather):
    return {
        "city": raw_weather["name"],
        "country": raw_weather["sys"]["country"],
        "temperature_c": raw_weather["main"]["temp"],
        "feels_like_c": raw_weather["main"]["feels_like"],
        "humidity": raw_weather["main"]["humidity"],
        "condition": raw_weather["weather"][0]["description"],
    }


def normalize_crypto(raw_crypto, coin_id, currency):
    coin = raw_crypto[coin_id]
    change_key = f"{currency}_24h_change"

    return {
        "coin": coin_id,
        "currency": currency.upper(),
        "price": coin[currency],
        "change_24h": coin.get(change_key),
    }


def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print("Saved data to", filename)


def main():
    load_dotenv()

    weather_api_key = os.getenv("WEATHER_API_KEY")
    city = os.getenv("CITY", "Mumbai")
    coin_id = os.getenv("COIN_ID", "bitcoin")
    currency = os.getenv("CURRENCY", "usd").lower()

    if weather_api_key is None:
        print("WEATHER_API_KEY was not found in .env")
        return

    raw_weather = fetch_weather(city, weather_api_key)
    raw_crypto = fetch_crypto(coin_id, currency)

    if raw_weather is None or raw_crypto is None:
        print("Could not fetch all required data.")
        return

    normalized = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "weather": normalize_weather(raw_weather),
        "crypto": normalize_crypto(raw_crypto, coin_id, currency),
    }

    save_json(normalized, "sample_output.json")
    print("Normalized data:", normalized)


if __name__ == "__main__":
    main()
