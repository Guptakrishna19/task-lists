import requests


# Exercise 3: Handle HTTP errors + timeouts
# We use requests.get() to call an API safely.
# If something goes wrong, the program should print a friendly message
# instead of crashing.


# --- 1. Function to fetch API data safely -------------------------------
def fetch_api_data(url, timeout_seconds=5):
    try:
        response = requests.get(url, timeout=timeout_seconds)

        # raise_for_status() catches HTTP errors like 404, 401, 500, etc.
        response.raise_for_status()

        data = response.json()
        print("Request successful!")
        print("Status code:", response.status_code)
        print("Data:", data)

    except requests.exceptions.Timeout:
        print("Timeout error: The request took too long.")

    except requests.exceptions.HTTPError as error:
        print("HTTP error:", error)

    except requests.exceptions.ConnectionError:
        print("Connection error: Check your internet or API URL.")

    except requests.exceptions.RequestException as error:
        print("Request error:", error)

    except ValueError:
        print("JSON error: Response is not valid JSON.")


# --- 2. Successful request ----------------------------------------------
print("\n1. Successful request")
success_url = "https://jsonplaceholder.typicode.com/posts/1"
fetch_api_data(success_url)


# --- 3. HTTP error request ----------------------------------------------
print("\n2. HTTP error request")
bad_url = "https://jsonplaceholder.typicode.com/wrong-url"
fetch_api_data(bad_url)


# --- 4. Timeout request --------------------------------------------------
print("\n3. Timeout request")
slow_url = "https://httpbin.org/delay/5"
fetch_api_data(slow_url, timeout_seconds=1)


# OUTPUT
"""
1. Successful request
Request successful!
Status code: 200
Data: {'userId': 1, 'id': 1, 'title': '...', 'body': '...'}

2. HTTP error request
HTTP error: 404 Client Error: Not Found for url: ...

3. Timeout request
Timeout error: The request took too long.
"""
