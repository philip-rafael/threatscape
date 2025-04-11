import requests
import json

# AbuseIPDB API Key
API_KEY = "f8bc9655f94f45aa796d4aa11d3500af6b78d266103f3f711eca23810f7147a6278aaf279b39352f"

# API URL
url = "https://api.abuseipdb.com/api/v2/blacklist"
params = {
    "confidenceMinimum": 50,  # Adjust this as needed
    "limit": 1000
}

# Set the headers with the API key
headers = {
    "Key": API_KEY,
    "Accept": "application/json"
}

# Fetch data from the API
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Save the response data to a file
    with open("cached_threat_data.json", "w") as f:
        json.dump(response.json(), f)
    print("Data saved successfully to cached_threat_data.json")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    print(response.text)
